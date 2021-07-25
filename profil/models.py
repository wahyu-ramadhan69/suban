from django.contrib.auth.models import Permission, User
from django.db import models
from django.db.models import Model
from datetime import MAXYEAR, datetime, date

from django.db.models.fields import IntegerField, PositiveIntegerField
from django.db.models.lookups import YearLookup


class penduduk(models.Model):
    nokk = models.CharField(max_length=20, null=True)
    nik = models.CharField(max_length=20, null=True, unique=True)
    nama = models.CharField(max_length=100, null=True)
    tempat_lahir = models.CharField(max_length=100, null=True, blank=True)
    tanggal_lahir = models.DateField(null=True, blank=True)
    status_perkawinan = models.CharField(max_length=50, null=True, blank=True)
    jk = models.CharField(max_length=10, null=True, blank=True)
    alamat = models.CharField(max_length=255, null=True, blank=True)
    rt = models.PositiveIntegerField(null=True, blank=True)
    dusun = models.PositiveIntegerField(null=True, blank=True)
    pekerjaan = models.CharField(max_length=50, null=True, blank=True)
    pendidikan = models.CharField(max_length=50, null=True, blank=True)

    @property
    def age(self):
        return int((datetime.now().date() - self.tanggal_lahir).days / 365.25)


class visi_misi(models.Model):
    visi = models.CharField(max_length=100, null=True, blank=True)
    misi = models.CharField(max_length=100, null=True, blank=True)


class informasi(models.Model):
    no = models.PositiveIntegerField(null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    link = models.CharField(max_length=255, null=True, blank=True)
    facebook = models.CharField(max_length=100, null=True, blank=True)
    instagram = models.CharField(max_length=100, null=True, blank=True)
    twiter = models.CharField(max_length=100, null=True, blank=True)
    whatsapp = models.CharField(max_length=100, null=True, blank=True)
    youtube = models.CharField(max_length=100, null=True, blank=True)
    tanggal = models.DateField(auto_now=True)

class berita(models.Model):
    judul = models.CharField(max_length=255,null=True,blank=True)
    deskripsi = models.TextField(null=True,blank=True)
    foto = models.FileField(upload_to='berita/',null=True,blank=True)
    author = models.CharField(max_length=100,null=True,blank=True)
    tanggal_diupload = models.DateField(auto_now_add=True)
    tanggal_diperbaharui = models.DateField(auto_now=True) 


class aparatur(models.Model):
    nama = models.CharField(max_length=100, null=True, blank=True)
    ttl = models.CharField(max_length=100, null=True, blank=True)
    jk = models.CharField(max_length=100, null=True, blank=True)
    pendidikan = models.CharField(max_length=100, null=True, blank=True)
    jabatan = models.CharField(max_length=100, null=True, blank=True)
    mulai_bekerja = models.CharField(max_length=100, null=True, blank=True)
    alamat = models.CharField(max_length=100, null=True, blank=True)
    keterangan = models.TextField(null=True, blank=True)
    foto = models.FileField(null=True, blank=True)
    bagian = models.PositiveIntegerField()

    def __str__(self):
        return self.nama

    def delete(self, *args, **kwargs):
        self.foto.delete()
        super().delete(*args, **kwargs)


class sturktur_aparatur(models.Model):
    foto = models.FileField(upload_to='struktur/', null=True, blank=True)
    bagian = models.PositiveIntegerField()

    def __str__(self):
        return self.nama

    def delete(self, *args, **kwargs):
        self.foto.delete()
        super().delete(*args, **kwargs)


class apbd_desa(models.Model):
    nama = models.CharField(max_length=256, null=True, blank=True)
    jumlah = models.CharField(max_length=100, null=True, blank=True)
    keterangan = models.TextField(null=True, blank=True)
    tanggal = models.DateField(auto_now_add=True, blank=True)
    kat = models.PositiveIntegerField()


class pariwisata(models.Model):
    nama = models.CharField(max_length=100, blank=True)
    lokasi = models.CharField(max_length=200, blank=True)
    foto = models.FileField(upload_to='wisata/', max_length=200, blank=True)
    keterangan = models.TextField(null=True, blank=True)
    author = models.CharField(max_length=100, null=True)
    tanggal = models.DateField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        self.foto.delete()
        super().delete(*args, **kwargs)


class budaya(models.Model):
    nama = models.CharField(max_length=100, blank=True)
    lokasi = models.CharField(max_length=200, blank=True)
    foto = models.FileField(upload_to='budaya/', max_length=200, blank=True)
    keterangan = models.TextField(null=True, blank=True)
    author = models.CharField(max_length=100, null=True)
    tanggal = models.DateField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        self.foto.delete()
        super().delete(*args, **kwargs)


class produk(models.Model):
    nama = models.CharField(max_length=100, blank=True)
    harga = models.PositiveIntegerField()
    nama_penjual = models.CharField(max_length=100, blank=True, null=True)
    no_wa = models.CharField(max_length=100, null=True, blank=True)
    deskripsi = models.TextField(null=True, blank=True)
    foto = models.FileField(upload_to='produk/', max_length=200, blank=True)
    author = models.CharField(max_length=100, null=True)
    tanggal = models.DateField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        self.foto.delete()
        super().delete(*args, **kwargs)


class covid(models.Model):
    suspek = models.PositiveIntegerField(null=True, blank=True)
    spesimen = models.PositiveIntegerField(null=True, blank=True)
    konfirmasi = models.PositiveIntegerField(null=True, blank=True)
    sembuh = models.PositiveIntegerField(null=True, blank=True)
    meninggal = models.PositiveIntegerField(null=True, blank=True)
    keterangan = models.TextField(null=True, blank=True)
    foto = models.FileField(upload_to='covid/', null=True, blank=True)
    author = models.CharField(max_length=150, null=True)
    tanggal = models.DateField(auto_now_add=True)


class sda(models.Model):
    nama = models.CharField(max_length=256, null=True, blank=True)
    luas = models.CharField(max_length=100, null=True, blank=True)
    keterangan = models.TextField(null=True, blank=True)
    tanggal = models.DateField(auto_now=True, blank=True)
    jenis = models.PositiveIntegerField()


class lembaga(models.Model):
    nama = models.CharField(max_length=200, null=True, blank=True)
    jumlah = models.PositiveIntegerField(null=True, blank=True)
    deskripsi = models.TextField(null=True, blank=True)
    jenis = models.PositiveIntegerField(null=True)


class prasarana(models.Model):
    nama = models.CharField(max_length=200, null=True, blank=True)
    jumlah = models.PositiveIntegerField(null=True, blank=True)
    deskripsi = models.TextField(null=True, blank=True)
    jenis = models.PositiveIntegerField(null=True)


class sdm(models.Model):
    nama = models.CharField(max_length=200, null=True, blank=True)
    jumlah = models.PositiveIntegerField(null=True, blank=True)
    jenis = models.PositiveIntegerField(null=True)
