from profil.models import penduduk
from import_export import resources
from .models import *


class penduduksum(resources.ModelResource):
    class Meta:
        model = penduduk
