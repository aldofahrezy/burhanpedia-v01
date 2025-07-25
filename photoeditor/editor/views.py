# editor/views.py

from django.shortcuts import render
from django.http import JsonResponse

# View untuk halaman utama (tetap sama)
def index_view(request):
    return render(request, 'editor/index.html')

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