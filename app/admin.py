from django.contrib import admin
from .models import Reporte, Material, SolicitudMaterial, DetalleSolicitud, Perfil

# Register your models here.
admin.site.register(Reporte)
admin.site.register(Material)
admin.site.register(DetalleSolicitud)
admin.site.register(SolicitudMaterial)
admin.site.register(Perfil)