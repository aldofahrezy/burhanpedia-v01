# kain_app/urls.py

from django.urls import path
from . import views

app_name = 'kain_app'

urlpatterns = [
    # URL untuk halaman utama
    path('', views.index, name='index'),
    # URL untuk halaman prediksi kain
    path('prediksi-kain/', views.prediksi_kain, name='prediksi_kain'),
    # URL untuk generator desain AI
    # URL ini menangani GET (menampilkan form) dan POST (menghasilkan gambar)
    path('create-kain/', views.create_kain, name='create_kain'),
]