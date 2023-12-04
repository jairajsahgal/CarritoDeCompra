from django.contrib import admin
from .models import Gorras,Camiseta,Tejido
# Register your models here.



admin.site.register([Camiseta,
                     Gorras,
                     Tejido])