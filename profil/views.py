from profil.forms import BA, FP, FPR, FVM, IMG, PA, PRO
from django.shortcuts import render, redirect, HttpResponse, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.html import format_html
from django.contrib.auth import login as auth_login
from .models import *
from django.db import IntegrityError
from .resources import *
from tablib import Dataset
from django.http import JsonResponse, request
import json
from django.db.models import Max
from django.contrib import messages

from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta

# controller user


def index(request):
    data = covid.objects.all().order_by('-id')
    Berita = berita.objects.all().order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(Berita, 6)
    try:
        datas = paginator.page(page)
    except PageNotAnInteger:
        datas = paginator.page(1)
    except EmptyPage:
        datas = paginator.page(paginator.num_pages)

    context = {
        'data': data,
        'datas' : datas,
        'page_title': 'Desa Suban Ayam',
    }
    return render(request, 'index.html', context)


def detail_covid(request, id):
    data = covid.objects.get(id=id)
    context = {
        'page_title': 'Detail covid-19 suban ayam',
        'data': data
    }
    return render(request, 'user/profil_desa/covid.html', context)


def informasi(request):
    data1 = penduduk.objects.count()
    context = {
        'data1': data1
    }
    return render(request, 'user/profil_desa/informasi.html', context)


def visi(request):
    data = visi_misi.objects.all()
    context = {
        'data': data
    }
    return render(request, 'user/profil_desa/visi.html', context)


def pariwisata_u(request):
    return render(request, 'user/pariwisata.html')


def kebudayaan(request):
    return render(request, 'user/kebudayaan.html')


def produk_u(request):
    return render(request, 'user/produk.html')


def perangkat_u(request):
    data = aparatur.objects.all().filter(bagian='1')
    gambar = sturktur_aparatur.objects.all().filter(bagian='1')
    if request.user.is_authenticated:
        form = IMG(request.POST or None,request.FILES or None)
        if request.method == 'POST':
            form.save()
            return redirect('perangkat_u')
    context = {
        'page_title': 'perangkat desa',
        'data': data,
        'gambar':gambar
    }
    return render(request, 'user/aparatur/perangkat.html', context)

def bpd_u(request):
    data = aparatur.objects.all().filter(bagian='2')
    gambar = sturktur_aparatur.objects.all().filter(bagian='2')
    if request.user.is_authenticated:
        form = IMG(request.POST or None,request.FILES or None)
        if request.method == 'POST':
            form.save()
            return redirect('bpd_u')
    context = {
        'page_title': 'perangkat bpd',
        'data': data,
        'gambar': gambar
    }
    return render(request, 'user/aparatur/bpd.html', context)

def agama_u(request):
    data = aparatur.objects.all().filter(bagian='3')
    gambar = sturktur_aparatur.objects.all().filter(bagian='3')
    if request.user.is_authenticated:
        form = IMG(request.POST or None,request.FILES or None)
        if request.method == 'POST':
            form.save()
            return redirect('agama_u')
    context = {
        'page_title': 'perangkat agama',
        'data': data,
        'gambar': gambar
    }
    return render(request, 'user/aparatur/agama.html', context)

def bma_u(request):
    data = aparatur.objects.all().filter(bagian='4')
    gambar = sturktur_aparatur.objects.all().filter(bagian='4')
    if request.user.is_authenticated:
        form = IMG(request.POST or None,request.FILES or None)
        if request.method == 'POST':
            form.save()
            return redirect('bma_u')
    context = {
        'page_title': 'perangkat bma',
        'data': data,
        'gambar': gambar
    }
    return render(request, 'user/aparatur/bma.html', context)

def kt_u(request):
    data = aparatur.objects.all().filter(bagian='5')
    gambar = sturktur_aparatur.objects.all().filter(bagian='5')
    if request.user.is_authenticated:
        form = IMG(request.POST or None,request.FILES or None)
        if request.method == 'POST':
            form.save()
            return redirect('kt_u')
    context = {
        'page_title': 'karang taruna',
        'data': data,
        'gambar': gambar
    }
    return render(request, 'user/aparatur/kt.html', context)

@login_required
def ubah_struk_perangkat(request):
    no = request.POST.get('bagian')
    data1 = sturktur_aparatur.objects.get(bagian=no)
    data2 = {
        'foto': data1.foto,
        'bagian': data1.bagian,
    }
    form = IMG(request.POST or None, request.FILES or None, initial=data2, instance=data1)
    if no == '1':
        if request.method == 'POST':
            form.save()
            return redirect('perangkat_u')
    elif no =='2':
        if request.method == 'POST':
            form.save()
            return redirect('bpd_u')
    elif no =='3':
        if request.method == 'POST':
            form.save()
            return redirect('agama_u')
    elif no =='4':
        if request.method == 'POST':
            form.save()
            return redirect('bma_u')
    elif no =='5':
        if request.method == 'POST':
            form.save()
            return redirect('kt_u')


def dana_u(request):
    data = apbd_desa.objects.all()
    data1 = apbd_desa.objects.all().filter(kat='1')
    data2 = apbd_desa.objects.all().filter(kat='2')
    data3 = apbd_desa.objects.all().filter(kat='3')
    data4 = apbd_desa.objects.all().filter(kat='4')
    data5 = apbd_desa.objects.all().filter(kat='5')
    data6 = apbd_desa.objects.all().filter(kat='6')
    context = {
        'page_title': 'APBD Desa',
        'data': data,
        'data1': data1,
        'data2': data2,
        'data3': data3,
        'data4': data4,
        'data5': data5,
        'data6': data6
    }
    return render(request, 'user/profil_desa/apbd.html', context)


def wisata_u(request):
    data = pariwisata.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(data, 6)
    try:
        datas = paginator.page(page)
    except PageNotAnInteger:
        datas = paginator.page(1)
    except EmptyPage:
        datas = paginator.page(paginator.num_pages)
    context = {
        'page_title': 'dana desa',
        'data': data,
        'datas': datas
    }
    return render(request, 'user/pariwisata.html', context)

def produk_u(request):
    data = produk.objects.all().order_by('-id')
    page = request.GET.get('page', 1)

    paginator = Paginator(data, 6)
    try:
        datas = paginator.page(page)
    except PageNotAnInteger:
        datas = paginator.page(1)
    except EmptyPage:
        datas = paginator.page(paginator.num_pages)
    context = {
        'page_title': 'produk desa suban ayam',
        'data': data,
        'datas': datas
    }
    return render(request, 'user/potensi/produk.html', context)

def detail_dana(request, id):
    data = dana_desa.objects.get(id=id)
    context = {
        'data': data
    }
    return render(request, 'user/dana_detail.html', context)


def sdm_u(request):
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

    data1 = sdm.objects.all().filter(jenis='1')
    data2 = sdm.objects.all().filter(jenis='2')
    data3 = sdm.objects.all().filter(jenis='3')
    data4 = sdm.objects.all().filter(jenis='4')
    data5 = sdm.objects.all().filter(jenis='5')
    data6 = sdm.objects.all().filter(jenis='6')
    data7 = sdm.objects.all().filter(jenis='7')

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

    tl = penduduk.objects.count()
    kk = penduduk.objects.values('nokk').distinct().count()
    jl = penduduk.objects.filter(jk='L').count()
    pr = penduduk.objects.filter(jk='P').count()
    sk = penduduk.objects.filter(status_perkawinan='S').count()
    bk = penduduk.objects.filter(status_perkawinan='B').count()
    
    context = {
        'kk': kk,
        'tl': tl,
        'jl': jl,
        'pr': pr,
        'sk': sk,
        'bk': bk,
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
        'page_title': 'Potensi penduduk'
    }
    return render(request, 'user/potensi/sdm.html', context)
# controller autenntikasi


def coba(request):
    context = {
        'page_title': 'percobaan'
    }
    return render(request, 'coba.html', context)


def sda_u(request):
    data = sda.objects.all()
    data1 = sda.objects.all().filter(jenis='1')
    data2 = sda.objects.all().filter(jenis='2')
    data3 = sda.objects.all().filter(jenis='3')
    data4 = sda.objects.all().filter(jenis='4')
    data5 = sda.objects.all().filter(jenis='5')
    data6 = sda.objects.all().filter(jenis='6')

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
    return render(request, 'user/potensi/sda.html', context)

def kelembagaan(request):
    data = lembaga.objects.all()
    data1 = lembaga.objects.all().filter(jenis='1')
    data2 = lembaga.objects.all().filter(jenis='2')
    data3 = lembaga.objects.all().filter(jenis='3')
    data4 = lembaga.objects.all().filter(jenis='4')
    data5 = lembaga.objects.all().filter(jenis='5')
    data6 = lembaga.objects.all().filter(jenis='6')

    context = {
        'page_title': 'Kelembagaan desa suban ayam',
        'data': data,
        'data1': data1,
        'data2': data2,
        'data3': data3,
        'data4': data4,
        'data5': data5,
        'data6': data6
    }
    return render(request, 'user/potensi/kelembagaan.html', context)

def pras_u(request):
    data = prasarana.objects.all()
    data1 = prasarana.objects.all().filter(jenis='1')
    data2 = prasarana.objects.all().filter(jenis='2')
    data3 = prasarana.objects.all().filter(jenis='3')
    data4 = prasarana.objects.all().filter(jenis='4')
    data5 = prasarana.objects.all().filter(jenis='5')
    data6 = prasarana.objects.all().filter(jenis='6')
    data7 = prasarana.objects.all().filter(jenis='7')
    data8 = prasarana.objects.all().filter(jenis='8')

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
    return render(request, 'user/potensi/prasarana.html', context)

def detail_berita(request,id):
    data = berita.objects.all().get(id=id)
    Berita = berita.objects.all().order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(Berita, 3)
    try:
        datas = paginator.page(page)
    except PageNotAnInteger:
        datas = paginator.page(1)
    except EmptyPage:
        datas = paginator.page(paginator.num_pages)
    context ={
        'data':data,
        'datas':datas,
        'page_title':'detail berita'
    }
    return render(request,'user/profil_desa/detail_berita.html',context)

def list_covid(request):
    data = covid.objects.all().order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(data, 6)
    try:
        datas = paginator.page(page)
    except PageNotAnInteger:
        datas = paginator.page(1)
    except EmptyPage:
        datas = paginator.page(paginator.num_pages)
    context ={
        'data':data,
        'datas':datas,
        'page_title':'Berita COVID-19'
    }
    return render(request,'user/profil_desa/informasi_covid.html',context)
