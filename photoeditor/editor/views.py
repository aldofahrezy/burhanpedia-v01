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

def generate_preview_ajax(request):
    """Memproses gambar via AJAX dan mengembalikan JSON."""
    if request.method == 'POST':
        form = ImageEditForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                base_image_file = form.cleaned_data['base_image']
                logo_image_file = form.cleaned_data.get('logo_image')
                text = form.cleaned_data.get('text')
                
                image = Image.open(base_image_file).convert("RGBA")
                
                if logo_image_file:
                    logo = Image.open(logo_image_file).convert("RGBA")
                    logo_w = form.cleaned_data.get('logo_w')
                    logo_h = form.cleaned_data.get('logo_h')
                    if logo_w and logo_h and logo_w > 0 and logo_h > 0:
                        logo = logo.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
                    image.paste(logo, (form.cleaned_data['logo_x'], form.cleaned_data['logo_y']), logo)

                if text:
                    draw = ImageDraw.Draw(image)
                    font_size = form.cleaned_data['font_size']
                    # Di sini kita perlu melakukan scaling font size juga
                    # Untuk sementara, kita gunakan nilai tetap, tapi idealnya dikirim dari JS
                    font = ImageFont.truetype("arial.ttf", font_size * 5) # Asumsi skala 5x
                    draw.text((form.cleaned_data['text_x'], form.cleaned_data['text_y']), text, font=font, fill="black")

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
            return JsonResponse({'success': False, 'error': 'Form tidak valid.'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})