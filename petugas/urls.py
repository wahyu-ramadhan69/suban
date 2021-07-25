from django.conf.urls import url, include
from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('', views.petugas, name='petugas'),
    path('penduduk', views.v_penduduk, name='penduduk'),
    path('penduduk/hapus_semua_penduduk',
         views.hapus_semua_penduduk, name='hapus_semua'),
    path('penduduk/simple_upload',
         views.simple_upload, name='simple_upload'),
    path('penduduk/hapus/<int:id>',
         views.hapus_penduduk, name='hapus_penduduk'),
    path('penduduk/ubah/<int:id>',
         views.ubah_penduduk, name='ubah_penduduk'),
    path('penduduk/cetak', views.cetak, name='cetak'),

    #     path('petugas/pariwisata', views.wisata, name='wisata'),
    #     path('petugas/pariwisata/ubah/<int:id>',
    #          views.ubah_wisata, name='ubah_wisata'),
    #     path('petugas/pariwisata/hapus/<int:id>',
    #          views.hapus_pariwisata, name='hapus_pariwisata'),

    #     path('petugas/budaya', views.kebudayaan2, name='kebudayaan2'),
    #     path('petugas/budaya/ubah/<int:id>',
    #          views.ubah_budaya, name='ubah_budaya'),
    #     path('petugas/budaya/hapus/<int:id>',
    #          views.hapus_budaya, name='hapus_budaya'),

    path('produk', views.prodak, name='prodak'),
    path('produk/ubah/<int:id>',
         views.ubah_prodak, name='ubah_prodak'),

    path('produk', views.produk, name='produk'),
    path('profil/visi_misi', views.visi_admin, name='visi_admin'),
    path('profil/visi_misi/ubah/<int:id>',
         views.ubah_visi, name='ubah_visi'),

    path('potensi/penduduk/filter', views.filter, name='filter'),

    path('profil/perangkat', views.perangkat_admin, name='perangkat_admin'),
    path('profil/bpd', views.bpd_admin, name='bpd_admin'),
    path('profil/perangkat_agama', views.agama, name='agama'),
    path('profil/perangkat_bma', views.bma, name='bma'),
    path('profil/karang_taruna', views.kt, name='kt'),

    path('profil/perangkat/ubah/<int:id>',
         views.ubah_perangkat, name='ubah_perangkat'),
    path('profil/perangkat/hapus/<int:id>',
         views.hapus_perangkat, name='hapus_perangkat'),

    path('profil/dana', views.dana, name='dana'),
    path('profil/dana/ubah/<int:id>',
         views.ubah_dana, name='ubah_dana'),
    path('profil/dana/hapus/<int:id>',
         views.hapus_dana, name='hapus_dana'),

     path('profil/berita', views.v_berita, name='v_berita'),
     path('profil/berita/ubah/<int:id>', views.ubah_berita, name='ubah_berita'),
     path('profil/berita/hapus/<int:id>', views.hapus_berita, name='hapus_berita'),

    path('profil/info_covid', views.info_covid, name='info_covid'),
    path('profil/info_covid/ubah/<int:id>', views.ubah_covid, name='ubah_covid'),
    path('profil/info_covid/hapus/<int:id>', views.hapus_covid, name='hapus_covid'),

    path('potensi/sda', views.sumberda, name='sumberda'),
    path('potensi/sda/ubah/<int:id>',
         views.ubah_sda, name='ubah_sda'),
    path('potensi/sda/hapus/<int:id>',
         views.hapus_sda, name='hapus_sda'),

    path('potensi/kelembagaan', views.lembaga_v, name='lembaga_v'),
    path('potensi/kelembagaan/ubah/<int:id>',
         views.ubah_lembaga, name='ubah_lembaga'),
    path('potensi/kelembagaan/hapus/<int:id>',
         views.hapus_lembaga, name='hapus_lembaga'),

    path('potensi/prasarana', views.pras, name='pras'),
    path('potensi/prasarana/ubah/<int:id>',
         views.ubah_pras, name='ubah_pras'),
    path('potensi/prasarana/hapus/<int:id>',
         views.hapus_pras, name='hapus_pras'),

    path('potensi/sdm', views.sumberdm, name='sumberdm'),
    path('potensi/sdm/ubah/<int:id>',
         views.ubah_sdm, name='ubah_sdm'),
    path('potensi/sdm/hapus/<int:id>',
         views.hapus_sdm, name='hapus_sdm'),
]
