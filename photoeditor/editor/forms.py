# editor/forms.py
from django import forms

class GenerateImageForm(forms.Form):
    prompt = forms.CharField(
        label="Deskripsikan gambar yang Anda inginkan",
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Contoh: Seekor astronot menunggang kuda di Mars, gaya surealis'})
    )

    # Choices for Batik Origin
    BATIK_ORIGIN_CHOICES = [
        ('', '-- Pilih Daerah Asal --'),
        ('Solo', 'Solo'),
        ('Yogyakarta', 'Yogyakarta'),
        ('Pekalongan', 'Pekalongan'),
        ('Cirebon', 'Cirebon'),
        ('Madura', 'Madura'),
        ('Bali', 'Bali'),
        ('Other', 'Lainnya (Tuliskan di deskripsi utama)') # Suggest adding to main prompt
    ]
    batik_origin = forms.ChoiceField(
        label="Preferensi Model Batik (Daerah Asal)",
        choices=BATIK_ORIGIN_CHOICES,
        required=False # Make it optional
    )

    # Choices for Batik Motif
    BATIK_MOTIF_CHOICES = [
        ('', '-- Pilih Motif --'),
        ('Parang', 'Parang'),
        ('Kawung', 'Kawung'),
        ('Mega Mendung', 'Mega Mendung'),
        ('Truntum', 'Truntum'),
        ('Sido Mukti', 'Sido Mukti'),
        ('Ceplok', 'Ceplok'),
        ('Other', 'Lainnya (Tuliskan di deskripsi utama)') # Suggest adding to main prompt
    ]
    batik_motif = forms.ChoiceField(
        label="Preferensi Model Batik (Motif)",
        choices=BATIK_MOTIF_CHOICES,
        required=False # Make it optional
    )

    custom_shape = forms.CharField(
        label="Preferensi Bentuk Tertentu (Bebas)",
        max_length=100, # Limit the length for custom shape
        required=False, # Make it optional
        widget=forms.TextInput(attrs={'placeholder': 'Contoh: geometris, bunga, hewan, abstrak'})
    )