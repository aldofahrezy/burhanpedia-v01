# editor/urls.py (buat file baru ini)
# editor/urls.py
# editor/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('create/', views.creative_mode_view, name='creative_mode'),
    path('quick/', views.quick_mode_view, name='quick_mode'),
    path('ajax/generate-preview/', views.generate_preview_ajax, name='ajax_generate_preview'),
    
    # --- TAMBAHKAN URL BARU INI ---
    path('generate/', views.generate_image_view, name='generate_image'),
]