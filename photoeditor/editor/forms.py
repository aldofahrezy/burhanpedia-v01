# editor/forms.py
from django import forms


class ImageEditForm(forms.Form):
    # Input yang terlihat oleh pengguna
    base_image = forms.ImageField(label="1. Unggah Gambar Utama", widget=forms.FileInput(attrs={'id': 'base_image_input'}))
    logo_image = forms.ImageField(label="2. Unggah Logo", required=False, widget=forms.FileInput(attrs={'id': 'logo_image_input'}))
    text = forms.CharField(label="3. Tambahkan Angka/Teks", required=False, widget=forms.TextInput(attrs={'id': 'text_input'}))
    font_size = forms.IntegerField(label="Ukuran Font di Preview", initial=50, required=False, widget=forms.NumberInput(attrs={'id': 'font_size_input'}))
    
    # --- PERBAIKAN DI SINI ---
    # Tambahkan `required=False` pada semua input tersembunyi
    text_x = forms.IntegerField(widget=forms.HiddenInput(attrs={'id': 'text_x_input'}), required=False)
    text_y = forms.IntegerField(widget=forms.HiddenInput(attrs={'id': 'text_y_input'}), required=False)
    logo_x = forms.IntegerField(widget=forms.HiddenInput(attrs={'id': 'logo_x_input'}), required=False)
    logo_y = forms.IntegerField(widget=forms.HiddenInput(attrs={'id': 'logo_y_input'}), required=False)
    logo_w = forms.IntegerField(widget=forms.HiddenInput(attrs={'id': 'logo_w_input'}), required=False)
    logo_h = forms.IntegerField(widget=forms.HiddenInput(attrs={'id': 'logo_h_input'}), required=False)

# (Class QuickEditForm di bawahnya tidak perlu diubah)

# editor/forms.py

# Tambahkan form baru ini di bawah form yang lama
class QuickEditForm(forms.Form):
    base_image = forms.ImageField(label="1. Unggah Gambar Jersey")
    logo_image = forms.ImageField(label="2. Unggah Logo", required=False)
    text = forms.CharField(label="3. Masukkan Angka/Teks", required=False)
    font_size = forms.IntegerField(label="Ukuran Teks", initial=150)

class GenerateImageForm(forms.Form):
    prompt = forms.CharField(
        label="Deskripsikan gambar yang Anda inginkan",
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Contoh: Seekor astronot menunggang kuda di Mars, gaya surealis'})
    )