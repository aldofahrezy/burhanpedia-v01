# kain_app/models.py

from django.db import models

class Kain(models.Model):
    """
    Model ini merepresentasikan data kain yang akan disimpan.
    """
    nama_kain = models.CharField(max_length=100)
    jenis_kain = models.CharField(max_length=50)
    warna = models.CharField(max_length=50)
    deskripsi = models.TextField(blank=True, null=True)
    tanggal_dibuat = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama_kain

    class Meta:
        verbose_name_plural = "Daftar Kain"