from django import forms
from django.contrib.auth.models import User
from django.db.models import fields
from profil.models import *


class FP(forms.ModelForm):
    class Meta:
        model = penduduk
        fields = ['nokk', 'nik', 'nama', 'tempat_lahir', 'tanggal_lahir',
                  'status_perkawinan', 'jk', 'alamat', 'rt', 'dusun', 'pekerjaan', 'pendidikan']


class FVM(forms.ModelForm):
    class Meta:
        model = visi_misi
        fields = ['visi', 'misi']


class FPR(forms.ModelForm):
    class Meta:
        model = aparatur
        fields = ['nama', 'ttl', 'jk', 'pendidikan',
                  'jabatan', 'mulai_bekerja', 'alamat', 'keterangan', 'foto']


class PA(forms.ModelForm):
    class Meta:
        model = pariwisata
        fields = ['nama', 'lokasi', 'foto', 'keterangan',
                  'author']


class BA(forms.ModelForm):
    class Meta:
        model = budaya
        fields = ['nama', 'lokasi', 'foto', 'keterangan',
                  'author']


class PRO(forms.ModelForm):
    class Meta:
        model = produk
        fields = ['nama', 'harga', 'nama_penjual', 'no_wa', 'deskripsi', 'foto',
                  'author']

class IMG(forms.ModelForm):
    class Meta:
        model = sturktur_aparatur
        fields = ['foto','bagian']
