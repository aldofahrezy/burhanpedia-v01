# editor/views.py

from django.shortcuts import render
from django.http import JsonResponse

# View untuk halaman utama (tetap sama)
def index_view(request):
    return render(request, 'editor/index.html')

# Pastikan import ini ada
from openai import OpenAI
from openai import APIStatusError, RateLimitError
from django.conf import settings
from .forms import GenerateImageForm # Pastikan form ini juga di-import
# ... import lainnya ...

def generate_image_view(request):
    result_image = None
    error_message = None

    if request.method == 'POST':
        form = GenerateImageForm(request.POST)
        if form.is_valid():

            # Base Prompt
            base_prompt = form.cleaned_data['prompt']

            # Preference Data
            batik_origin = form.cleaned_data['batik_origin']
            batik_motif = form.cleaned_data['batik_motif']
            custom_shape = form.cleaned_data['custom_shape']
            
            # --- Construct the dynamic prompt ---
            full_prompt_parts = []

            # Add the base prompt first
            if base_prompt:
                full_prompt_parts.append(base_prompt)

            # Add batik details if selected
            batik_description_parts = []
            if batik_origin and batik_origin != "Other":
                batik_description_parts.append(f"Batik {batik_origin}")
            # If "Other" is selected, the user should put details in the main prompt
            # so we don't need a separate handling here unless you add a specific text input for "Other"

            if batik_motif and batik_motif != "Other":
                batik_description_parts.append(f"motif {batik_motif}")
            # Same for "Other" motif

            if batik_description_parts:
                full_prompt_parts.append(" ".join(batik_description_parts))

            # Add custom shape if provided
            if custom_shape:
                full_prompt_parts.append(f"dengan bentuk {custom_shape}")

            # Combine all parts into the final prompt for DALL-E 3
            # Use a comma as a separator, ensuring proper sentence structure
            final_prompt = ", ".join(full_prompt_parts).strip()

            # Ensure the prompt is not empty; provide a fallback if necessary
            if not final_prompt:
                final_prompt = "sebuah gambar" # Default fallback prompt

            print(f"Final prompt for DALL-E 3: {final_prompt}") # For debugging purposes
            try:
                # 1. Buat client OpenAI dan otentikasi menggunakan kunci dari settings.py
                client = OpenAI(api_key=settings.OPENAI_API_KEY)

                # 2. Lakukan panggilan API ke DALL-E 3
                response = client.images.generate(
                    model="dall-e-3",
                    prompt= final_prompt,
                    size="1024x1024",
                    quality="standard",
                    n=1,
                    response_format="b64_json"
                )

                # 3. Ambil data gambar dari respons
                result_image = response.data[0].b64_json

            except RateLimitError:
                error_message = "Anda telah mencapai batas kuota. Silakan cek akun OpenAI Anda."
            except APIStatusError as e:
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