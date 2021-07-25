from django import forms
from profil.models import *


class FTA(forms.ModelForm):
    class Meta:
        model = aparatur
        fields = ['nama', 'ttl', 'jk', 'pendidikan',
                  'jabatan', 'mulai_bekerja', 'alamat', 'keterangan', 'foto', 'bagian']


class APBD(forms.ModelForm):
    class Meta:
        model = apbd_desa
        fields = ['nama', 'jumlah', 'keterangan', 'kat']


class APBDD(forms.ModelForm):
    class Meta:
        model = apbd_desa
        fields = ['nama', 'jumlah', 'keterangan']


class SDA(forms.ModelForm):
    class Meta:
        model = sda
        fields = ['nama', 'luas', 'keterangan', 'jenis']


class SDAA(forms.ModelForm):
    class Meta:
        model = sda
        fields = ['nama', 'luas', 'keterangan']


class COV(forms.ModelForm):
    class Meta:
        model = covid
        fields = ['suspek', 'spesimen', 'konfirmasi', 'sembuh',
                  'meninggal', 'keterangan', 'foto', 'author']


class LEM(forms.ModelForm):
    class Meta:
        model = lembaga
        fields = ['nama', 'jumlah', 'deskripsi', 'jenis']


class LEMB(forms.ModelForm):
    class Meta:
        model = lembaga
        fields = ['nama', 'jumlah', 'deskripsi']


class PRA(forms.ModelForm):
    class Meta:
        model = prasarana
        fields = ['nama', 'jumlah', 'deskripsi', 'jenis']


class PRAS(forms.ModelForm):
    class Meta:
        model = prasarana
        fields = ['nama', 'jumlah', 'deskripsi']


class SDM(forms.ModelForm):
    class Meta:
        model = sdm
        fields = ['nama', 'jumlah', 'jenis']


class SDMM(forms.ModelForm):
    class Meta:
        model = sdm
        fields = ['nama', 'jumlah']

class BERITA(forms.ModelForm):
    class Meta:
        model = berita
        fields =['judul','deskripsi','foto','author']
