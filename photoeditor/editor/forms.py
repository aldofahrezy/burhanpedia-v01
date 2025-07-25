# editor/forms.py
from django import forms

class GenerateImageForm(forms.Form):
    prompt = forms.CharField(
        label="Deskripsikan gambar yang Anda inginkan",
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Contoh: Seekor astronot menunggang kuda di Mars, gaya surealis'})
    )