# editor/views.py

from django.shortcuts import render
from .forms import ImageEditForm, QuickEditForm # Pastikan keduanya di-import
from PIL import Image, ImageDraw, ImageFont
from django.http import JsonResponse
import io
import base64

# View untuk halaman utama (tetap sama)
def index_view(request):
    return render(request, 'editor/index.html')

# View untuk mode cepat (tetap sama)
def quick_mode_view(request):
    # ... (kode untuk quick_mode_view tidak perlu diubah) ...
    result_image = None
    if request.method == 'POST':
        form = QuickEditForm(request.POST, request.FILES)
        if form.is_valid():
            image = Image.open(form.cleaned_data['base_image']).convert("RGBA")
            if form.cleaned_data.get('logo_image'):
                logo = Image.open(form.cleaned_data['logo_image']).convert("RGBA")
                logo_w = image.width // 5
                logo.thumbnail((logo_w, logo_w))
                logo_x = int(image.width * 0.65)
                logo_y = int(image.height * 0.15)
                image.paste(logo, (logo_x, logo_y), logo)
            if form.cleaned_data.get('text'):
                draw = ImageDraw.Draw(image)
                font_size = form.cleaned_data['font_size']
                font = ImageFont.truetype("arial.ttf", font_size)
                text_bbox = draw.textbbox((0, 0), form.cleaned_data['text'], font=font)
                text_w = text_bbox[2] - text_bbox[0]
                text_x = (image.width - text_w) // 2
                text_y = int(image.height * 0.25)
                draw.text((text_x, text_y), form.cleaned_data['text'], font=font, fill="black")
            
            if image.mode in ("RGBA", "P"): image = image.convert("RGB")
            buffer = io.BytesIO()
            image.save(buffer, format='JPEG', quality=95)
            result_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
    else:
        form = QuickEditForm()
    return render(request, 'editor/quick_mode.html', {'form': form, 'result_image': result_image})


# --- PERBARUI FUNGSI INI ---
# editor/views.py

# (index_view dan quick_mode_view tetap di sini...)

def creative_mode_view(request):
    """Hanya menampilkan halaman editor interaktif."""
    form = ImageEditForm()
    return render(request, 'editor/creative_mode.html', {'form': form})
# editor/views.py

def generate_preview_ajax(request):
    """Memproses gambar via AJAX dan mengembalikan JSON."""
    if request.method == 'POST':
        form = ImageEditForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # ... (logika untuk base_image dan logo tetap sama) ...
                base_image_file = form.cleaned_data['base_image']
                logo_image_file = form.cleaned_data.get('logo_image')
                text = form.cleaned_data.get('text')
                image = Image.open(base_image_file).convert("RGBA")

                if logo_image_file:
                    # ... (logika paste logo tidak berubah) ...
                    logo = Image.open(logo_image_file).convert("RGBA")
                    logo_w = form.cleaned_data.get('logo_w')
                    logo_h = form.cleaned_data.get('logo_h')
                    if logo_w and logo_h and logo_w > 0 and logo_h > 0:
                        logo = logo.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
                    image.paste(logo, (form.cleaned_data['logo_x'], form.cleaned_data['logo_y']), logo)
                
                # --- PERBAIKAN LOGIKA FONT DI SINI ---
                if text:
                    draw = ImageDraw.Draw(image)
                    # Gunakan ukuran font yang sudah diskalakan dari frontend
                    scaled_font_size = form.cleaned_data.get('scaled_font_size')
                    
                    if scaled_font_size:
                        font = ImageFont.truetype("arial.ttf", scaled_font_size)
                        draw.text((form.cleaned_data['text_x'], form.cleaned_data['text_y']), text, font=font, fill="black")

                # ... (sisa logika untuk resize final dan save ke JPEG tetap sama) ...
                max_size = (1024, 1024)
                image.thumbnail(max_size, Image.Resampling.LANCZOS)
                if image.mode in ("RGBA", "P"): image = image.convert("RGB")
                buffer = io.BytesIO()
                image.save(buffer, format='JPEG', quality=95)
                result_image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
                
                return JsonResponse({'success': True, 'image_data': result_image_base64})
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})
        else:
            # Kirim detail error form untuk debugging
            return JsonResponse({'success': False, 'error': 'Form tidak valid.', 'errors': form.errors.as_json()})
            
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

# editor/views.py

# Pastikan import ini ada
import openai
from django.conf import settings
from .forms import GenerateImageForm # Pastikan form ini juga di-import
# ... import lainnya ...

def generate_image_view(request):
    result_image = None
    error_message = None

    if request.method == 'POST':
        form = GenerateImageForm(request.POST)
        if form.is_valid():
            prompt = form.cleaned_data['prompt']
            try:
                # 1. Buat client OpenAI dan otentikasi menggunakan kunci dari settings.py
                client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

                # 2. Lakukan panggilan API ke DALL-E 3
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    size="1024x1024",
                    quality="standard",
                    n=1,
                    response_format="b64_json" # Minta hasil dalam format base64
                )

                # 3. Ambil data gambar dari respons
                result_image = response.data[0].b64_json

            except openai.RateLimitError:
                error_message = "Anda telah mencapai batas kuota. Silakan cek akun OpenAI Anda."
            except openai.APIStatusError as e:
                error_message = f"Error dari OpenAI: {e.status_code} - {e.response.text}"
            except Exception as e:
                error_message = f"Terjadi kesalahan: {e}"
    else:
        form = GenerateImageForm()

    # Jangan lupa update template yang digunakan jika perlu
    return render(request, 'editor/generate_image.html', {
        'form': form,
        'result_image': result_image,
        'error': error_message
    })