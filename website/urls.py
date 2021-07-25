from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.views import debug
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('petugas/', include('petugas.urls')),
    path('', include('profil.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
