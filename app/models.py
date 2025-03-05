from django.db import models

# Create your models here.

class Reporte(models.Model):
    # Campos que puede rellenar el usuario
    fecha = models.DateField()
    sucursal = models.CharField(max_length=50)
    clasificacion = models.CharField(max_length=50)
    equipo = models.CharField(max_length=50)
    reporte = models.CharField(max_length=50)
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

