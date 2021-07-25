from petugas.forms import APBD, APBDD, BERITA, COV, FTA, LEM, LEMB, PRA, PRAS, SDA, SDAA, SDM, SDMM
from profil.forms import BA, FP, FPR, FVM, PA, PRO
from profil.resources import penduduksum
from django.shortcuts import render, redirect, HttpResponse, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.html import avoid_wrapping, format_html
from django.contrib.auth import login as auth_login
from xlwt.Formatting import Font
import xlwt
from profil.models import *
from django.db import IntegrityError
from tablib import Dataset
from django.http import JsonResponse, request
import json
from django.db.models import Max
from django.contrib import messages
import datetime
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta

# controller untuk admin


def login(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('petugas')
        else:
            return render(request, 'auth/login.html')
    if request.method == "POST":
        user = None
        username_login = request.POST['username']
        password_login = request.POST['password']

        user = authenticate(request, username=username_login,
                            password=password_login)

        if user is not None:
            auth_login(request, user)
            return redirect('petugas')
        else:
            messages.error(request, 'username atau password salah')
            return redirect('login')


def logout_user(request):
    logout(request)
    return redirect('/')


def petugas(request):
    if request.user.is_authenticated:
        data1 = penduduk.objects.count()
        context = {
            'page_title': 'desa suban ayam',
            'data1': data1,
            'warna': 'primary'
        }
        return render(request, 'admin/index.html', context)
    else:
        return redirect('login')


def simple_upload(request):
    if request.method == 'POST':
        kubsum = penduduksum()
        dataset = Dataset()
        dataset = Dataset()
        data = request.FILES['myfile']
        imported_data = dataset.load(data.read(), format='xlsx')
        # print(imported_data)
        for data in imported_data:
            print(data[1])
            value = penduduk(
                data[0],
                data[1],
                data[2],
                data[3],
                data[4],
                data[5],
                data[6],
                data[7],
                data[8],
                data[9],
                data[10],
                data[11],
                data[12],
            )
            value.save()
    return redirect('penduduk')


@login_required
def v_penduduk(request):
    data = penduduk.objects.all().filter(dusun=0)
    kk = penduduk.objects.values('nokk').distinct().count()
    print(kk)
    context = {
        'warna': 'info',
        'page_title': 'Data penduduk suban ayam dusun 0',
        'data': data
    }
    if request.method == 'POST':
        simpan = FP(request.POST or None)
        if simpan.is_valid():
            simpan.save()
            messages.success(request, "Data penduduk berhasil di input")
            return redirect('penduduk')
        else:
            messages.error(request, "Nik sudah pernah di daftarkan")
            return redirect('penduduk')
    return render(request, 'admin/penduduk.html', context)


@login_required
def hapus_penduduk(request, id):
    penduduk.objects.filter(id=id).delete()
    messages.success(request, "Data penduduk berhasil di hapus")
    return redirect('penduduk')


@login_required
def ubah_penduduk(request, id):
    data1 = penduduk.objects.get(id=id)
    data2 = {
        'nokk': data1.nokk,
        'nik': data1.nik,
        'nama': data1.nama,
        'tempat_lahir': data1.tempat_lahir,
        'tanggal_lahir': data1.tanggal_lahir,
        'status_perkawinan': data1.status_perkawinan,
        'jk': data1.jk,
        'alamat': data1.alamat,
        'rt': data1.rt,
        'dusun': data1.dusun,
        'pekerjaan': data1.pekerjaan,
        'pendidikan': data1.pendidikan,
    }
    simpan = FP(request.POST or None, request.FILES or None,
                initial=data2, instance=data1)
    if request.method == 'POST':
        if simpan.is_valid():
            simpan.save()
            messages.success(request, "Data penduduk berhasil di ubah")
            return redirect('penduduk')
        else:
            messages.error(request, "Data penduduk tidak berhasil di ubah")
            return redirect('penduduk')


@login_required
def hapus_semua_penduduk(request):
    if request.user.is_superuser == 1:
        penduduk.objects.all().delete()
        messages.success(request, 'Data seluruh penduduk berhasil di hapus')
        return redirect('penduduk')
    else:
        messages.error(request, 'Kamu tidak memiliki hak akses untuk aksi ini')
        return redirect('penduduk')


@login_required
def produk_u(request):
    return render(request, 'admin/produk.html')


@login_required
def visi_admin(request):
    data = visi_misi.objects.all()
    context = {
        'warna': 'primary',
        'page_title': 'visi misi',
        'data': data
    }
    return render(request, 'admin/profildesa/visi.html', context)


@login_required
def filter(request):
    no = request.POST.get('no')
    if no == '7':
        data = penduduk.objects.all()
        context = {
            'warna': 'info',
            'page_title': 'Data penduduk suban ayam',
            'data': data
        }
        return render(request, 'admin/penduduk.html', context)
    else:
        data = penduduk.objects.all().filter(dusun=no)
        context = {
            'warna': 'info',
            'page_title': 'Data penduduk suban ayam dusun ' + no,
            'data': data
        }
        return render(request, 'admin/penduduk.html', context)

    data = penduduk.objects.all().filter(dusun=0)
    context = {
        'warna': 'info',
        'page_title': 'Data penduduk suban ayam dusun ' + no,
        'data': data
    }
    return render(request, 'admin/penduduk.html', context)


@login_required
def cetak(request):
    f = request.POST.get('format')
    n = request.POST.get('no')
    if f == '1':
        if n == '1':
            data = penduduk.objects.all().filter(dusun=n)
            context = {
                'dusun': '1',
                'data': data
            }
            return render(request, 'admin/cetak.html', context)
        elif n == '0':
            data = penduduk.objects.all().filter(dusun=n)
            context = {
                'dusun': '0',
                'data': data
            }
            return render(request, 'admin/cetak.html', context)
        elif n == '2':
            data = penduduk.objects.all().filter(dusun=n)
            context = {
                'dusun': '2',
                'data': data
            }
            return render(request, 'admin/cetak.html', context)
        elif n == '3':
            data = penduduk.objects.all().filter(dusun=n)
            context = {
                'dusun': '3',
                'data': data
            }
            return render(request, 'admin/cetak.html', context)
        elif n == '4':
            data = penduduk.objects.all().filter(dusun=n)
            context = {
                'dusun': '4',
                'data': data
            }
            return render(request, 'admin/cetak.html', context)
        elif n == '5':
            data = penduduk.objects.all().filter(dusun=n)
            context = {
                'dusun': '5',
                'data': data
            }
            return render(request, 'admin/cetak.html', context)
        elif n == '6':
            data = penduduk.objects.all().filter(dusun=n)
            context = {
                'dusun': '6',
                'data': data
            }
            return render(request, 'admin/cetak.html', context)
        elif n == '7':
            data = penduduk.objects.all()
            context = {
                'dusun': '',
                'data': data
            }
            return render(request, 'admin/cetak.html', context)
        else:
            return redirect('penduduk')
    elif f == '2':
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=data_penduduk_suban_ayam' + \
            str(datetime.now())+'.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('penduduk')

        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['No', 'Nomor KK', 'Nik', 'Nama', 'Tempat lahir', 'Tanggal lahir',
                   'Status_perkawinan', 'Jk', 'Alamat', 'Rt', 'Dusun', 'Pekerjaan', 'Pendidikan']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        font_style = xlwt.XFStyle()

        rows = penduduk.objects.values_list(
            'id', 'nokk', 'nik', 'nama', 'tempat_lahir', 'tanggal_lahir',
                  'status_perkawinan', 'jk', 'alamat', 'rt', 'dusun', 'pekerjaan', 'pendidikan')

        for row in rows:
            row_num += 1

            for col_num in range(len(row)):
                ws.write(row_num, col_num, str(row[col_num]), font_style)
        wb.save(response)

        return response
    else:
        return redirect('penduduk')


@login_required
def ubah_visi(request, id):
    data1 = visi_misi.objects.get(id=id)
    data2 = {
        'nokk': data1.visi,
        'nik': data1.misi,
    }
    simpan = FVM(request.POST or None, request.FILES or None,
                 initial=data2, instance=data1)
    if request.method == 'POST':
        if simpan.is_valid():
            simpan.save()
            messages.success(request, "Data visi misi di ubah")
            return redirect('visi_admin')
        else:
            messages.error(request, "Data visi misi tidak berhasil di ubah")
            return redirect('visi_admin')


@login_required
def perangkat_admin(request):
    data = aparatur.objects.all().filter(bagian='1')
    simpan = FTA(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if simpan.is_valid():
            simpan.save()
            messages.success(request, "Data perangkat berhasil ditambahkan")
            return redirect('perangkat_admin')
        else:
            messages.error(request, "Data perangkat gagal ditambahkan")
            return redirect('perangkat_admin')
    context = {
        'warna': 'warning',
        'page_title': 'perangkat desa',
        'data': data
    }
    return render(request, 'admin/aparatur/perangkat.html', context)


@login_required
def bpd_admin(request):
    data = aparatur.objects.all().filter(bagian='2')
    simpan = FTA(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if simpan.is_valid():
            simpan.save()
            messages.success(request, "Data bpd berhasil ditambahkan")
            return redirect('bpd_admin')
        else:
            messages.error(request, "Data bpd  gagal ditambahkan")
            return redirect('bpd_admin')
    context = {
        'warna': 'warning',
        'page_title': 'perangkat bpd',
        'data': data
    }
    return render(request, 'admin/aparatur/bpd.html', context)


@login_required
def agama(request):
    data = aparatur.objects.all().filter(bagian='3')
    simpan = FTA(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if simpan.is_valid():
            simpan.save()
            messages.success(
                request, "Data perangkat agama berhasil ditambahkan")
            return redirect('agama')
        else:
            messages.error(request, "Data perangkat agama  gagal ditambahkan")
            return redirect('agama')
    context = {
        'page_title': 'perangkat agama',
        'warna': 'warning',
        'data': data
    }
    return render(request, 'admin/aparatur/agama.html', context)


@login_required
def bma(request):
    data = aparatur.objects.all().filter(bagian='4')
    simpan = FTA(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if simpan.is_valid():
            simpan.save()
            messages.success(
                request, "Data perangkat bma berhasil ditambahkan")
            return redirect('bma')
        else:
            messages.error(request, "Data perangkat bma  gagal ditambahkan")
            return redirect('bma')
    context = {
        'page_title': 'perangkat bma',
        'warna': 'warning',
        'data': data
    }
    return render(request, 'admin/aparatur/bma.html', context)

@login_required
def kt(request):
    data = aparatur.objects.all().filter(bagian='5')
    simpan = FTA(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if simpan.is_valid():
            simpan.save()
            messages.success(
                request, "Data karang taruna berhasil ditambahkan")
            return redirect('kt')
        else:
            messages.error(request, "Data karang taruna gagal ditambahkan")
            return redirect('kt')
    context = {
        'page_title': 'karang taruna',
        'warna': 'warning',
        'data': data
    }
    return render(request, 'admin/aparatur/kt.html', context)


@login_required
def ubah_perangkat(request, id):
    data1 = aparatur.objects.get(id=id)
    data2 = {
        'nama': data1.nama,
        'ttl': data1.ttl,
        'jk': data1.jk,
        'pendidikan': data1.pendidikan,
        'jabatan': data1.jabatan,
        'mulai_bekerja': data1.mulai_bekerja,
        'alamat': data1.alamat,
        'keterangan': data1.keterangan,
        'foto': data1.foto,
    }
    no = request.POST.get('bagian')
    if no == '1':
        simpan = FPR(request.POST or None, request.FILES or None,
                     initial=data2, instance=data1)
        if request.method == 'POST':
            if simpan.is_valid():
                simpan.save()
                messages.success(request, "Data perangkat berhasil di ubah")
                return redirect('perangkat_admin')
            else:
                messages.error(
                    request, "Data perangkat tidak berhasil di ubah")
                return redirect('perangkat_admin')
    elif no == '2':
        simpan = FPR(request.POST or None, request.FILES or None,
                     initial=data2, instance=data1)
        if request.method == 'POST':
            if simpan.is_valid():
                simpan.save()
                messages.success(request, "Data bpd berhasil di ubah")
                return redirect('bpd_admin')
            else:
                messages.error(request, "Data bpd tidak berhasil di ubah")
                return redirect('bpd_admin')

    elif no == '3':
        simpan = FPR(request.POST or None, request.FILES or None,
                     initial=data2, instance=data1)
        if request.method == 'POST':
            if simpan.is_valid():
                simpan.save()
                messages.success(
                    request, "Data perangkat agama berhasil di ubah")
                return redirect('agama')
            else:
                messages.error(
                    request, "Data perangkat agama tidak berhasil di ubah")
                return redirect('agama')
    elif no == '4':
        simpan = FPR(request.POST or None, request.FILES or None,
                     initial=data2, instance=data1)
        if request.method == 'POST':
            if simpan.is_valid():
                simpan.save()
                messages.success(
                    request, "Data perangkat bma berhasil di ubah")
                return redirect('bma')
            else:
                messages.error(
                    request, "Data perangkat bma tidak berhasil di ubah")
                return redirect('bma')
    elif no == '5':
        simpan = FPR(request.POST or None, request.FILES or None,
                     initial=data2, instance=data1)
        if request.method == 'POST':
            if simpan.is_valid():
                simpan.save()
                messages.success(
                    request, "Data karang taruna berhasil di ubah")
                return redirect('kt')
            else:
                messages.error(
                    request, "Data karang taruna tidak berhasil di ubah")
                return redirect('kt')


@login_required
def hapus_perangkat(request, id):
    no = request.POST.get('bagian')
    if no == '1':
        aparatur.objects.get(id=id).delete()
        messages.success(request, "Data perangkat berhasil di hapus")
        return redirect('perangkat_admin')
    elif no == '2':
        aparatur.objects.get(id=id).delete()
        messages.success(request, "Data bpd berhasil di hapus")
        return redirect('bpd_admin')
    elif no == '3':
        aparatur.objects.get(id=id).delete()
        messages.success(request, "Data perangkat agama berhasil di hapus")
        return redirect('agama')
    elif no == '4':
        aparatur.objects.get(id=id).delete()
        messages.success(request, "Data perangkat bma berhasil di hapus")
        return redirect('bma')
    elif no == '5':
        aparatur.objects.get(id=id).delete()
        messages.success(request, "Data karang taruna berhasil di hapus")
        return redirect('kt')


@login_required
def dana(request):
    data = apbd_desa.objects.all()
    data1 = apbd_desa.objects.all().filter(kat='1')
    data2 = apbd_desa.objects.all().filter(kat='2')
    data3 = apbd_desa.objects.all().filter(kat='3')
    data4 = apbd_desa.objects.all().filter(kat='4')
    data5 = apbd_desa.objects.all().filter(kat='5')
    data6 = apbd_desa.objects.all().filter(kat='6')
    form = APBD(request.POST or None)
    no = request.POST.get('kat')
    if request.method == 'POST':
        if no == '1':
            if form.is_valid():
                form.save()
                messages.success(
                    request, 'data pendapatan desa berhasil ditambahkan')
                return redirect('dana')
            else:
                messages.error(
                    request, 'data pendapatan desa gagal ditambahkan')
                return redirect('dana')
        elif no == '2':
            if form.is_valid():
                form.save()
                messages.success(
                    request, 'data Penyelenggaraan Pemerintahan Desa berhasil ditambahkan')
                return redirect('dana')
            else:
                messages.error(
                    request, 'data Penyelenggaraan Pemerintahan Desa gagal ditambahkan')
                return redirect('dana')
        elif no == '3':
            if form.is_valid():
                form.save()
                messages.success(
                    request, 'data Pembangunan Desa berhasil ditambahkan')
                return redirect('dana')
            else:
                messages.error(
                    request, 'data Pembangunan Desa gagal ditambahkan')
                return redirect('dana')
        elif no == '4':
            if form.is_valid():
                form.save()
                messages.success(
                    request, 'data Pembinaan Kemasyarakatan berhasil ditambahkan')
                return redirect('dana')
            else:
                messages.error(
                    request, 'data Pembinaan Kemasyarakatan gagal ditambahkan')
                return redirect('dana')
        elif no == '5':
            if form.is_valid():
                form.save()
                messages.success(
                    request, 'data Pemberdayaan masyarakat berhasil ditambahkan')
                return redirect('dana')
            else:
                messages.error(
                    request, 'data Pemberdayaan masyarakat gagal ditambahkan')
                return redirect('dana')
        elif no == '6':
            if form.is_valid():
                form.save()
                messages.success(
                    request, 'data Penanggulanagan bencana, darurat dan mendesak berhasil ditambahkan')
                return redirect('dana')
            else:
                messages.error(
                    request, 'data Penanggulangan bencana, darurat dan mendesak gagal ditambahkan')
                return redirect('dana')
        else:
            messages.error(request, 'gagal!!')
            return redirect('dana')

    context = {
        'warna': 'primary',
        'page_title': 'APBD Desa',
        'data': data,
        'data1': data1,
        'data2': data2,
        'data3': data3,
        'data4': data4,
        'data5': data5,
        'data6': data6
    }
    return render(request, 'admin/profildesa/apbd.html', context)


@login_required
def ubah_dana(request, id):
    data1 = apbd_desa.objects.get(id=id)
    data2 = {
        'nama': data1.nama,
        'jumlah': data1.jumlah,
        'keterangan': data1.keterangan,
    }
    simpan = APBDD(request.POST or None, request.FILES or None,
                   initial=data2, instance=data1)
    if request.method == 'POST':
        if simpan.is_valid():
            simpan.save()
            messages.success(request, "Data apbd desa berhasil di ubah")
            return redirect('dana')
        else:
            messages.error(request, "Data apbd desa tidak berhasil di ubah")
            return redirect('dana')


@login_required
def hapus_dana(request, id):
    apbd_desa.objects.get(id=id).delete()
    messages.success(request, "Data apbd desa berhasil di hapus")
    return redirect('dana')


@login_required
def hapus_budaya(request, id):
    budaya.objects.get(id=id).delete()
    messages.success(request, "Data budaya berhasil di hapus")
    return redirect('kebudayaan2')


def sumberda(request):
    data = sda.objects.all()
    data1 = sda.objects.all().filter(jenis='1')
    data2 = sda.objects.all().filter(jenis='2')
    data3 = sda.objects.all().filter(jenis='3')
    data4 = sda.objects.all().filter(jenis='4')
    data5 = sda.objects.all().filter(jenis='5')
    data6 = sda.objects.all().filter(jenis='6')
    form = SDA(request.POST or None)
    no = request.POST.get('jenis')
    if no == '1':
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(
                    request, 'Data Sumber daya pertanian berhasil ditambah')
                return redirect('sumberda')
            else:
                messages.error(request, 'Sumber daya pertanian gagal ditambah')
                return redirect('sumberda')
    elif no == '2':
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(
                    request, 'Data Sumber daya perkebunan berhasil ditambah')
                return redirect('sumberda')
            else:
                messages.error(
                    request, 'Sumber daya perkebunan gagal ditambah')
                return redirect('sumberda')
    elif no == '3':
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(
                    request, 'Data Sumber daya peternakan berhasil ditambah')
                return redirect('sumberda')
            else:
                messages.error(
                    request, 'Sumber daya peternakan gagal ditambah')
                return redirect('sumberda')
    elif no == '4':
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(
                    request, 'Data Sumber daya perikanan berhasil ditambah')
                return redirect('sumberda')
            else:
                messages.error(
                    request, 'Sumber daya perikanan gagal ditambah')
                return redirect('sumberda')
    elif no == '5':
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(
                    request, 'Data Sumber daya air berhasil ditambah')
                return redirect('sumberda')
            else:
                messages.error(
                    request, 'Sumber daya air gagal ditambah')
                return redirect('sumberda')
    elif no == '6':
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(
                    request, 'Data lahan gembala berhasil ditambah')
                return redirect('sumberda')
            else:
                messages.error(
                    request, 'lahan gembala gagal ditambah')
                return redirect('sumberda')
    context = {
        'page_title': 'Sumber Daya Alam Desa Suban Ayam',
        'warna': 'info',
        'data': data,
        'data1': data1,
        'data2': data2,
        'data3': data3,
        'data4': data4,
        'data5': data5,
        'data6': data6
    }
    return render(request, 'admin/potensi/sda.html', context)


@login_required
def ubah_sda(request, id):
    data1 = sda.objects.get(id=id)
    data2 = {
        'nama': data1.nama,
        'luas': data1.luas,
        'keterangan': data1.keterangan,
    }
    simpan = SDAA(request.POST or None, request.FILES or None,
                  initial=data2, instance=data1)
    if request.method == 'POST':
        if simpan.is_valid():
            simpan.save()
            messages.success(request, "Data sumber daya berhasil di ubah")
            return redirect('sumberda')
        else:
            messages.error(request, "Data sumber daya tidak berhasil di ubah")
            return redirect('sumberda')


@login_required
def hapus_sda(request, id):
    sda.objects.get(id=id).delete()
    messages.success(request, "Data sda desa berhasil di hapus")
    return redirect('sumberda')


@login_required
def lembaga_v(request):
    data = lembaga.objects.all()
    data1 = lembaga.objects.all().filter(jenis='1')
    data2 = lembaga.objects.all().filter(jenis='2')
    data3 = lembaga.objects.all().filter(jenis='3')
    data4 = lembaga.objects.all().filter(jenis='4')
    data5 = lembaga.objects.all().filter(jenis='5')
    data6 = lembaga.objects.all().filter(jenis='6')
    form = LEM(request.POST or None)
    no = request.POST.get('jenis')
    if no == '1':
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(
                    request, 'Data lembaga pemerintahan berhasil ditambah')
                return redirect('lembaga_v')
            else:
                messages.error(request, 'lembaga pemerintahan gagal ditambah')
                return redirect('lembaga_v')
    elif no == '2':
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(
                    request, 'Data lembaga kemasyarakatan berhasil ditambah')
                return redirect('lembaga_v')
            else:
                messages.error(
                    request, 'lembaga kemasyarakatan gagal ditambah')
                return redirect('lembaga_v')
    elif no == '3':
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(
                    request, 'Data lembaga ekonomi berhasil ditambah')
                return redirect('lembaga_v')
            else:
                messages.error(
                    request, 'lembaga ekonomi gagal ditambah')
                return redirect('lembaga_v')
    elif no == '4':
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(
                    request, 'Data lembaga pendidikan berhasil ditambah')
                return redirect('lembaga_v')
            else:
                messages.error(
                    request, 'lembaga pendidikan gagal ditambah')
                return redirect('lembaga_v')
    elif no == '5':
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(
                    request, 'Data lembaga adat berhasil ditambah')
                return redirect('lembaga_v')
            else:
                messages.error(
                    request, 'lembaga adat gagal ditambah')
                return redirect('lembaga_v')
    elif no == '6':
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(
                    request, 'Data lembaga keamanan berhasil ditambah')
                return redirect('lembaga_v')
            else:
                messages.error(
                    request, 'lembaga keamanan gagal ditambah')
                return redirect('lembaga_v')
    context = {
        'page_title': 'Kelembagaan desa suban ayam',
        'warna': 'info',
        'data': data,
        'data1': data1,
        'data2': data2,
        'data3': data3,
        'data4': data4,
        'data5': data5,
        'data6': data6
    }
    return render(request, 'admin/potensi/lembaga.html', context)


@login_required
def ubah_lembaga(request, id):
    data1 = lembaga.objects.get(id=id)
    data2 = {
        'nama': data1.nama,
        'jumlah': data1.jumlah,
        'deskripsi': data1.deskripsi,
    }
    simpan = LEMB(request.POST or None, request.FILES or None,
                  initial=data2, instance=data1)
    if request.method == 'POST':
        if simpan.is_valid():
            simpan.save()
            messages.success(request, "Data kelembagaan berhasil di ubah")
            return redirect('lembaga_v')
        else:
            messages.error(request, "Data kelembagaan tidak berhasil di ubah")
            return redirect('lembaga_v')


@login_required
def hapus_lembaga(request, id):
    lembaga.objects.get(id=id).delete()
    messages.success(request, "Data kelembagaan berhasil di hapus")
    return redirect('lembaga_v')


@login_required
def pras(request):
    data = prasarana.objects.all()
    data1 = prasarana.objects.all().filter(jenis='1')
    data2 = prasarana.objects.all().filter(jenis='2')
    data3 = prasarana.objects.all().filter(jenis='3')
    data4 = prasarana.objects.all().filter(jenis='4')
    data5 = prasarana.objects.all().filter(jenis='5')
    data6 = prasarana.objects.all().filter(jenis='6')
    data7 = prasarana.objects.all().filter(jenis='7')
    data8 = prasarana.objects.all().filter(jenis='8')
    form = PRA(request.POST or None)
    no = request.POST.get('jenis')
    if no == '1':
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(
                    request, 'Data prasarana transportasi darat berhasil ditambah')
                return redirect('pras')
            else:
                messages.error(
                    request, 'prasarana transportasi darat gagal ditambah')
                return redirect('pras')
    elif no == '2':
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(
                    request, 'Data prasarana komunikasi berhasil ditambah')
                return redirect('pras')
            else:
                messages.error(
                    request, 'prasarana komunikasi gagal ditambah')
                return redirect('pras')
    elif no == '3':
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(
                    request, 'Data prasarana air bersih berhasil ditambah')
                return redirect('pras')
            else:
                messages.error(
                    request, 'prasarana air bersih gagal ditambah')
                return redirect('pras')
    elif no == '4':
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(
                    request, 'Data prasarana irigasi berhasil ditambah')
                return redirect('pras')
            else:
                messages.error(
                    request, 'prasarana irigasi gagal ditambah')
                return redirect('pras')
    elif no == '5':
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(
                    request, 'Data prasarana peribadatan berhasil ditambah')
                return redirect('pras')
            else:
                messages.error(
                    request, 'prasarana peribadatan ditambah')
                return redirect('pras')
    elif no == '6':
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(
                    request, 'Data prasarana pemerintahan berhasil ditambah')
                return redirect('pras')
            else:
                messages.error(
                    request, 'prasarana pemerintahan gagal ditambah')
                return redirect('pras')
    elif no == '7':
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(
                    request, 'Data prasarana kesehatan berhasil ditambah')
                return redirect('pras')
            else:
                messages.error(
                    request, 'prasarana kesehatan gagal ditambah')
                return redirect('pras')
    elif no == '8':
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(
                    request, 'Data prasarana penerangan berhasil ditambah')
                return redirect('pras')
            else:
                messages.error(
                    request, 'prasarana penerangan gagal ditambah')
                return redirect('pras')
    context = {
        'page_title': 'Prasarana desa suban ayam',
        'warna': 'info',
        'data': data,
        'data1': data1,
        'data2': data2,
        'data3': data3,
        'data4': data4,
        'data5': data5,
        'data6': data6,
        'data7': data7,
        'data8': data8
    }
    return render(request, 'admin/potensi/prasarana.html', context)


@login_required
def ubah_pras(request, id):
    data1 = prasarana.objects.get(id=id)
    data2 = {
        'nama': data1.nama,
        'jumlah': data1.jumlah,
        'deskripsi': data1.deskripsi,
    }
    simpan = PRAS(request.POST or None, request.FILES or None,
                  initial=data2, instance=data1)
    if request.method == 'POST':
        if simpan.is_valid():
            simpan.save()
            messages.success(request, "Data prasarana berhasil di ubah")
            return redirect('pras')
        else:
            messages.error(request, "Data prasarana tidak berhasil di ubah")
            return redirect('pras')


@login_required
def hapus_pras(request, id):
    prasarana.objects.get(id=id).delete()
    messages.success(request, "Data prasarana berhasil di hapus")
    return redirect('pras')


@login_required
def prodak(request):
    data = produk.objects.all()
    if request.method == 'POST':
        no = request.POST.get('no_wa')
        simpan = PRO(request.POST or None, request.FILES or None)
        if simpan.is_valid():
            simpan.no_wa = '62' + str(no)
            simpan.save()
            messages.success(request, "Data Produk berhasil ditambah")
            return redirect('prodak')
        else:
            messages.error(request, "Data Produk gagal ditambah")
            return redirect('prodak')
    context = {
        'page_title': 'Produk suban ayam',
        'warna':'info',
        'data': data
    }
    return render(request, 'admin/produk.html', context)


@login_required
def ubah_prodak(request, id):
    data1 = produk.objects.get(id=id)
    data2 = {
        'nama': data1.nama,
        'harga': data1.harga,
        'nama_penjual': data1.nama_penjual,
        'no_wa': data1.no_wa,
        'deskripsi': data1.deskripsi,
        'foto': data1.foto
    }
    simpan = PRO(request.POST or None, request.FILES or None,
                 initial=data2, instance=data1)
    if request.method == 'POST':
        if simpan.is_valid():
            simpan.save()
            messages.success(request, "Data Produk desa berhasil di ubah")
            return redirect('prodak')
        else:
            messages.error(
                request, "Data Produk tidak berhasil di ubah")
            return redirect('prodak')


@login_required
def info_covid(request):
    data = covid.objects.all().order_by('-id')
    form = COV(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(
                request, "informasi coviid terbaru berhasil diunggah")
            return redirect('info_covid')
        else:
            messages.error(request, "informasi coviid terbaru gagal diunggah")
            return redirect('info_covid')

    context = {
        'warna': 'primary',
        'page_title': 'Informasi Covid-19',
        'data': data
    }
    return render(request, 'admin/profildesa/covid.html', context)

@login_required
def ubah_covid(request, id):
    data1 = covid.objects.get(id=id)
    data2 = {
        'suspek': data1.suspek,
        'spesimen': data1.spesimen,
        'konfirmasi': data1.konfirmasi,
        'sembuh': data1.sembuh,
        'meninggal': data1.meninggal,
        'keterangan': data1.keterangan,
        'foto': data1.foto,
        'author': data1.author,
    }
    simpan = COV(request.POST or None, request.FILES or None,initial=data2, instance=data1)
    if request.method == 'POST':
        if simpan.is_valid():
            simpan.save()
            messages.success(request, "Data informasi covid desa berhasil di ubah")
            return redirect('info_covid')
        else:
            messages.error(
                request, "Data informasi covid tidak berhasil di ubah")
            return redirect('info_covid')

@login_required
def hapus_covid(request, id):
    covid.objects.get(id=id).delete()
    messages.success(request, "Data informasi covid berhasil di hapus")
    return redirect('info_covid')


@login_required
def sumberdm(request):
    sekarang = date.today()
    umur10 = date.today() - relativedelta(years=10)
    umur11 = date.today() - relativedelta(years=10)
    umur20 = date.today() - relativedelta(years=20)
    umur21 = date.today() - relativedelta(years=20)
    umur30 = date.today() - relativedelta(years=30)
    umur31 = date.today() - relativedelta(years=30)
    umur40 = date.today() - relativedelta(years=40)
    umur41 = date.today() - relativedelta(years=40)
    umur50 = date.today() - relativedelta(years=50)
    umur51 = date.today() - relativedelta(years=50)
    umur60 = date.today() - relativedelta(years=60)
    umur61 = date.today() - relativedelta(years=60)
    umur70 = date.today() - relativedelta(years=70)

    umur1 = penduduk.objects.all().filter(
        tanggal_lahir__range=[umur10, sekarang]).count()
    umur2 = penduduk.objects.all().filter(
        tanggal_lahir__range=[umur20, umur11]).count()
    umur3 = penduduk.objects.all().filter(
        tanggal_lahir__range=[umur30, umur21]).count()
    umur4 = penduduk.objects.all().filter(
        tanggal_lahir__range=[umur40, umur31]).count()
    umur5 = penduduk.objects.all().filter(
        tanggal_lahir__range=[umur50, umur41]).count()
    umur6 = penduduk.objects.all().filter(
        tanggal_lahir__range=[umur60, umur51]).count()
    umur7 = penduduk.objects.all().filter(
        tanggal_lahir__range=[umur70, umur61]).count()
    umur8 = penduduk.objects.all().filter(tanggal_lahir__lte=umur70).count()
    data = sdm.objects.all()
    data1 = sdm.objects.all().filter(jenis='1')
    data2 = sdm.objects.all().filter(jenis='2')
    data3 = sdm.objects.all().filter(jenis='3')
    data4 = sdm.objects.all().filter(jenis='4')
    data5 = sdm.objects.all().filter(jenis='5')
    data6 = sdm.objects.all().filter(jenis='6')
    data7 = sdm.objects.all().filter(jenis='7')
    form = SDM(request.POST or None)
    no = request.POST.get('jenis')
    if no == '7':
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(
                    request, 'Data penduduk masih sekolah berhasil ditambah')
                return redirect('sumberdm')
            else:
                messages.error(
                    request, 'penduduk masih sekolah gagal ditambah')
                return redirect('sumberdm')
    elif no == '2':
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(
                    request, 'Data pendidikan penduduk berhasil ditambah')
                return redirect('sumberdm')
            else:
                messages.error(
                    request, 'pendidikan penduduk gagal ditambah')
                return redirect('sumberdm')
    elif no == '3':
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(
                    request, 'Data pendapatan pokok penduduk berhasil ditambah')
                return redirect('sumberdm')
            else:
                messages.error(
                    request, 'pendapatan pokok penduduk gagal ditambah')
                return redirect('sumberdm')
    elif no == '4':
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(
                    request, 'Data agama penduduk berhasil ditambah')
                return redirect('sumberdm')
            else:
                messages.error(
                    request, 'agama penduduk gagal ditambah')
                return redirect('sumberdm')
    elif no == '5':
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(
                    request, 'Data penduduk cacat berhasil ditambah')
                return redirect('sumberdm')
            else:
                messages.error(
                    request, 'penduduk cacat ditambah')
                return redirect('sumberdm')
    elif no == '6':
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(
                    request, 'Data tenaga kerja berhasil ditambah')
                return redirect('sumberdm')
            else:
                messages.error(
                    request, 'tenaga kerja gagal ditambah')
                return redirect('sumberdm')
    context = {
        'data': data,
        'data1': data1,
        'data2': data2,
        'data3': data3,
        'data4': data4,
        'data5': data5,
        'data6': data6,
        'data7': data7,
        'umur1': umur1,
        'umur2': umur2,
        'umur3': umur3,
        'umur4': umur4,
        'umur5': umur5,
        'umur6': umur6,
        'umur7': umur7,
        'umur8': umur8,
        'page_title': 'sumber daya manusia desa suban ayam',
        'warna': 'info'
    }
    return render(request, 'admin/potensi/sdm.html', context)


@login_required
def ubah_sdm(request, id):
    data1 = sdm.objects.get(id=id)
    data2 = {
        'nama': data1.nama,
        'jumlah': data1.jumlah,
    }
    simpan = SDMM(request.POST or None, request.FILES or None,
                  initial=data2, instance=data1)
    if request.method == 'POST':
        if simpan.is_valid():
            simpan.save()
            messages.success(request, "Data potensi sdm berhasil di ubah")
            return redirect('sumberdm')
        else:
            messages.error(request, "Data potensi sdm tidak berhasil di ubah")
            return redirect('sumberdm')


@login_required
def hapus_sdm(request, id):
    sdm.objects.get(id=id).delete()
    messages.success(request, "Data potensi sdm berhasil di hapus")
    return redirect('sumberdm')

@login_required
def v_berita(request):
    data = berita.objects.all().order_by('-id')
    form = BERITA(request.POST or None,request.FILES or None)
    if request.method == 'POST':
        if form.is_valid:
            form.save()
            messages.success(request,"berita berhasil di upload")
            return redirect('v_berita')
        else :
            messages.error(request,"berita berhasil di upload")
            return redirect('v_berita')
    context ={
        'data':data,
        'warna' : 'primary',
        'page_title': 'Berita suban ayam'
    }
    return render(request,'admin/profildesa/berita.html',context)

@login_required
def ubah_berita(request, id):
    data1 = berita.objects.get(id=id)
    data2 = {
        'judul': data1.judul,
        'deskripsi': data1.deskripsi,
        'foto': data1.foto,
        'author': data1.author,
    }
    form = BERITA(request.POST or None, request.FILES or None,
                  initial=data2, instance=data1)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Artikel berita berhasil di ubah")
            return redirect('v_berita')
        else:
            messages.error(request, "Artikel berita tidak berhasil di ubah")
            return redirect('v_berita')

@login_required
def hapus_berita(request, id):
    berita.objects.get(id=id).delete()
    messages.success(request, "Data berita berhasil di hapus")
    return redirect('v_berita')

# @login_required
# def wisata(request):
#     data = pariwisata.objects.all()
#     if request.method == 'POST':
#         simpan = PA(request.POST or None, request.FILES or None)
#         if simpan.is_valid():
#             simpan.save()
#             messages.success(request, "Data Pariwisata berhasil ditambah")
#             return redirect('wisata')
#         else:
#             messages.error(request, "Data Pariwisata gagal ditambah")
#             return redirect('wisata')
#     context = {
#         'page_title': 'Pariwisata',
#         'data': data
#     }
#     return render(request, 'admin/pariwisata.html', context)


# @login_required
# def ubah_wisata(request, id):
#     data1 = pariwisata.objects.get(id=id)
#     data2 = {
#         'nama': data1.nama,
#         'lokasi': data1.lokasi,
#         'foto': data1.foto,
#         'keterangan': data1.keterangan
#     }
#     simpan = PA(request.POST or None, request.FILES or None,
#                 initial=data2, instance=data1)
#     if request.method == 'POST':
#         if simpan.is_valid():
#             simpan.save()
#             messages.success(request, "Data wisata desa berhasil di ubah")
#             return redirect('wisata')
#         else:
#             messages.error(request, "Data wisata desa tidak berhasil di ubah")
#             return redirect('wisata')


# @login_required
# def hapus_pariwisata(request, id):
#     pariwisata.objects.get(id=id).delete()
#     messages.success(request, "Data wisata berhasil di hapus")
#     return redirect('wisata')


# @login_required
# def kebudayaan2(request):
#     data = budaya.objects.all()
#     if request.method == 'POST':
#         simpan = BA(request.POST or None, request.FILES or None)
#         if simpan.is_valid():
#             simpan.save()
#             messages.success(request, "Data Budaya berhasil ditambah")
#             return redirect('kebudayaan2')
#         else:
#             messages.error(request, "Data Budaya gagal ditambah")
#             return redirect('kebudayaan2')
#     context = {
#         'page_title': 'Kebudayaan',
#         'data': data
#     }
#     return render(request, 'admin/budaya.html', context)


# @login_required
# def ubah_budaya(request, id):
#     data1 = budaya.objects.get(id=id)
#     data2 = {
#         'nama': data1.nama,
#         'lokasi': data1.lokasi,
#         'foto': data1.foto,
#         'keterangan': data1.keterangan
#     }
#     simpan = BA(request.POST or None, request.FILES or None,
#                 initial=data2, instance=data1)
#     if request.method == 'POST':
#         if simpan.is_valid():
#             simpan.save()
#             messages.success(request, "Data Kebudayan desa berhasil di ubah")
#             return redirect('kebudayaan2')
#         else:
#             messages.error(
#                 request, "Data Kebudayaan desa tidak berhasil di ubah")
#             return redirect('kebudayaan2')
