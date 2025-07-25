# kain_app/views.py

import os
import base64
import json
from django.shortcuts import render
from openai import OpenAI
from dotenv import load_dotenv

# Muat environment variables dari file .env
load_dotenv()

# Inisialisasi client OpenAI
try:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except Exception as e:
    print(f"Error initializing OpenAI client: {e}")
    client = None

# Daftar preferensi untuk Generator Desain (tidak berubah)
BATIK_OPTIONS = [
    "Parang", "Kawung", "Megamendung", "Sidomukti", "Truntum", "Sogan", 
    "Lasem", "Pekalongan", "Garutan", "Tujuh Rupa", "Sekar Jagad", 
    "Tambal", "Cuwiri", "Pola Nitik", "Ceplok"
]
WARNA_OPTIONS = [
    "Merah Marun dan Emas", "Biru Laut dan Perak", "Hijau Zamrud dan Cokelat",
    "Hitam dan Putih Klasik", "Ungu Royal dan Lavender", "Oranye Senja dan Kuning",
    "Palet Warna Pastel", "Monokromatik Biru", "Warna Tanah (Earth Tones)", "Warna Cerah Tropis"
]

def index(request):
    return render(request, 'kain_app/index.html')

def prediksi_kain(request):
    """
    Menangani upload gambar, mengirimkannya ke OpenAI Vision untuk dianalisis,
    dan menampilkan hasilnya dalam format terstruktur.
    """
    context = {
        'analysis_result': None,
        'error_message': None,
        'uploaded_image': None
    }

    if not client:
        context['error_message'] = "Kunci API OpenAI tidak dikonfigurasi. Harap periksa file .env Anda."
        return render(request, 'kain_app/prediksi_kain.html', context)

    if request.method == 'POST' and request.FILES.get('gambar_kain'):
        image_file = request.FILES['gambar_kain']
        
        # Validasi sederhana untuk tipe file gambar
        if not image_file.content_type.startswith('image'):
            context['error_message'] = "File yang diunggah harus dalam format gambar (contoh: JPG, PNG)."
            return render(request, 'kain_app/prediksi_kain.html', context)
            
        # Encode gambar ke format base64 agar bisa dikirim via JSON
        try:
            image_read = image_file.read()
            base64_image = base64.b64encode(image_read).decode('utf-8')
            image_data_url = f"data:{image_file.content_type};base64,{base64_image}"
            context['uploaded_image'] = image_data_url
        except Exception as e:
            context['error_message'] = f"Gagal memproses file gambar: {e}"
            return render(request, 'kain_app/prediksi_kain.html', context)


        # Prompt yang dirancang untuk mendapatkan output JSON yang terstruktur dari AI
        prompt_text = """
        Anda adalah seorang ahli tekstil dan budaya Indonesia. Analisis gambar yang saya berikan.
        1.  Pertama, tentukan apakah gambar tersebut adalah kain atau tekstil berpola, khususnya yang menyerupai batik atau kain tradisional Indonesia.
        2.  Jika BUKAN kain/tekstil, kembalikan JSON dengan format: {"is_kain": false, "analysis": null}. JANGAN berikan penjelasan lain.
        3.  Jika IYA adalah kain/tekstil, identifikasi nama pola atau gayanya. Kemudian, berikan analisis mendalam.
        4.  Kemas analisis dalam format JSON yang ketat sebagai berikut:
            {
              "is_kain": true,
              "pattern_name": "Nama Pola/Gaya Kain yang Paling Sesuai",
              "analysis": {
                "origin": "Jelaskan asal-usul daerah atau budaya dari pola ini.",
                "colors": "Jelaskan palet warna yang umum digunakan pada pola ini dan maknanya jika ada.",
                "philosophy": "Jelaskan filosofi atau makna simbolis di balik setiap elemen motif tersebut.",
                "story": "Sajikan cerita atau sejarah singkat yang terkait dengan penciptaan atau penggunaan kain ini dalam budaya."
              }
            }
        Pastikan respons Anda HANYA berupa JSON yang valid tanpa teks tambahan atau penanda seperti ```json.
        """

        try:
            # Mengirim request ke API OpenAI dengan model Vision terbaru
            response = client.chat.completions.create(
                model="gpt-4o",  # Menggunakan model Vision terbaru dan tercepat
                response_format={ "type": "json_object" }, # Memaksa output menjadi format JSON
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt_text},
                            {
                                "type": "image_url",
                                "image_url": {"url": image_data_url, "detail": "low"},
                            },
                        ],
                    }
                ],
                max_tokens=1500,
            )

            # Ekstrak dan parse respons JSON dari AI
            analysis_result = json.loads(response.choices[0].message.content)
            context['analysis_result'] = analysis_result

        except json.JSONDecodeError:
            context['error_message'] = "Gagal membaca respons dari AI. Format yang diterima tidak valid."
        except Exception as e:
            print(f"OpenAI API error: {e}")
            context['error_message'] = f"Maaf, terjadi kesalahan saat menganalisis gambar: {e}"

    return render(request, 'kain_app/prediksi_kain.html', context)


def create_kain(request):
    """
    Menangani form input untuk generasi gambar batik dan menampilkan hasilnya (tidak berubah).
    """
    context = {
        'batik_options': BATIK_OPTIONS,
        'warna_options': WARNA_OPTIONS,
        'image_url': None,
        'prompt': None,
        'error_message': None
    }

    if not client:
        context['error_message'] = "Kunci API OpenAI tidak dikonfigurasi dengan benar. Silakan periksa file .env Anda."
        return render(request, 'kain_app/create_kain.html', context)

    if request.method == 'POST':
        batik_pilihan = request.POST.get('batik')
        warna_pilihan = request.POST.get('warna')
        bentuk_campuran = request.POST.get('bentuk_campuran')
        mockup_pilihan = request.POST.get('mockup')

        prompt = (
            f"Desain kain batik modern dan artistik, terinspirasi dari motif '{batik_pilihan}', "
            f"menggunakan palet warna dominan '{warna_pilihan}'. "
            f"Gabungkan dengan elemen '{bentuk_campuran}'. "
            f"Gunakan mockup '{mockup_pilihan}' untuk presentasi dengan fotorealistik, dan detail tinggi."
        )
        
        context['prompt'] = prompt

        try:
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            image_url = response.data[0].url
            context['image_url'] = image_url
        except Exception as e:
            print(f"OpenAI API error: {e}")
            context['error_message'] = f"Maaf, terjadi kesalahan saat menghasilkan gambar: {e}"

    return render(request, 'kain_app/create_kain.html', context)

def splash_1(request):
    """
    Menangani tampilan splash screen (tidak berubah).
    """
    return render(request, 'kain_app/splash/splash_1.html')

def splash_2(request):
    """
    Menangani tampilan splash screen (tidak berubah).
    """
    return render(request, 'kain_app/splash/splash_2.html')

def splash_3(request):
    """
    Menangani tampilan splash screen (tidak berubah).
    """
    return render(request, 'kain_app/splash/splash_3.html')

def splash_4(request):
    """
    Menangani tampilan splash screen (tidak berubah).
    """
    return render(request, 'kain_app/splash/splash_4.html')

def splash_5(request):
    """
    Menangani tampilan splash screen (tidak berubah).
    """
    return render(request, 'kain_app/splash/splash_5.html')