from django.urls import path
from . import views

app_name = 'kain_app'

urlpatterns = [
    # Change the root URL to start with splash_1
    path('', views.splash_1, name='root_splash'), # New: this is your initial landing page
    
    # Existing URL for the actual index page, accessed after splash screens
    path('index/', views.index, name='index'), # Changed: now explicitly '/index/'
    
    # URL for halaman prediksi kain
    path('prediksi-kain/', views.prediksi_kain, name='prediksi_kain'),
    # URL for generator desain AI
    path('create-kain/', views.create_kain, name='create_kain'),
    
    # Splash screens (now with explicits paths as they are part of the sequence)
    path('splash-1/', views.splash_1, name='splash_1'),
    path('splash-2/', views.splash_2, name='splash_2'),
    path('splash-3/', views.splash_3, name='splash_3'),
    path('splash-4/', views.splash_4, name='splash_4'),
    path('splash-5/', views.splash_5, name='splash_5'),
    path('museum/', views.museum, name='museum'),
    path('events/', views.events, name='events'),
]