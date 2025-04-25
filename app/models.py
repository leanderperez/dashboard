from django.db import models
from django.contrib.auth.models import User
import uuid

class Reporte(models.Model):
    # Campos que puede rellenar el usuario
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='reportes')
    fecha = models.DateField()
    sucursal = models.CharField(max_length=50)
    clasificacion = models.CharField(max_length=50)
    equipo = models.CharField(max_length=50)
    reporte = models.CharField(max_length=75)
    falla = models.CharField(max_length=50)
    coordinador = models.CharField(max_length=50)
    estatus = models.BooleanField(default=False)
    urgencia = models.CharField(max_length=50, null=True)
    
    # Campos para ser llenados por un administrador
    referencia = models.CharField(max_length=50, blank=True, null=True)
    personal = models.CharField(max_length=50, blank=True, null=True)
    encargado = models.CharField(max_length=50, blank=True, null=True)
    refrigerante = models.CharField(max_length=50, blank=True, null=True)
    kilos = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fecha_cierre = models.DateField(blank=True, null=True)
    costo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    gasto = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    ods_pdf = models.FileField(upload_to='pdfs/', blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

class Material(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    unidad_medida = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class SolicitudMaterial(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_solicitud = models.DateField(auto_now_add=True)
    sucursal = models.CharField(max_length=50)
    observaciones = models.TextField(blank=True, null=True)
    aprobada = models.BooleanField(default=False)
    completado = models.BooleanField(default=False)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # Token único

    def __str__(self):
        return f"Solicitud #{self.id} - {self.usuario.username}"

class DetalleSolicitud(models.Model):
    solicitud = models.ForeignKey(SolicitudMaterial, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.material.nombre} - {self.cantidad}"
