from django.conf.urls import url, include
from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profil/visimisi', views.visi, name='visi'),
    path('pariwisata', views.pariwisata_u, name='pariwisata_u'),
    path('kebudayaan', views.kebudayaan, name='kebudayaan'),
    path('produk', views.produk_u, name='produk_u'),
    path('profil/petadesa', views.informasi, name='informasi'),
    path('profil/apbd_desa', views.dana_u, name='dana_u'),
    path('profil/keuangandesa/detail/<int:id>',
         views.detail_dana, name='detail_dana'),

     path('profil/detail_berita/<int:id>', views.detail_berita, name='detail_berita'),

    path('informasi_covid/detail/<int:id>',
         views.detail_covid, name='detail_covid'),
    path('profil/berita_covid', views.list_covid, name='list_covid'),

    path('potensi/pariwisata', views.wisata_u, name='wisata_u'),

    path('potensi/sdm', views.sdm_u, name='sdm_u'),
    path('potensi/sda', views.sda_u, name='sda_u'),
    path('potensi/lembaga', views.kelembagaan, name='kelembagaan'),
     path('potensi/prasarana', views.pras_u, name='pras_u'),
     path('potensi/produk', views.produk_u, name='produk_u'),

     path('aparatur/perangkat', views.perangkat_u, name='perangkat_u'),
     path('aparatur/bpd', views.bpd_u, name='bpd_u'),
     path('aparatur/agama', views.agama_u, name='agama_u'),
     path('aparatur/bma', views.bma_u, name='bma_u'),
     path('aparatur/kt', views.kt_u, name='kt_u'),
     path('aparatur/ubah_struktur_perangkat', views.ubah_struk_perangkat, name='ubah_struk_perangkat'),

    path('coba', views.coba, name='coba'),
]
