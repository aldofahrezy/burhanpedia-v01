# editor/urls.py (buat file baru ini)
# editor/urls.py
# editor/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('generate/', views.generate_image_view, name='generate_image'),
]