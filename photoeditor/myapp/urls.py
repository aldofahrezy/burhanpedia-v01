from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('', views.index, name='prediksi_index'),
    path('save-label/', views.save_label_view, name='save_label')
]
