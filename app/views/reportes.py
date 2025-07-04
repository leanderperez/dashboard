from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from app.views.login import is_coordinador
from app.forms.forms import ReporteForm, ReporteAdminForm
from app.models import Reporte
from datetime import datetime

@login_required
def crear_reporte(request):
    # Verifica si el usuario es coordinador
    if is_coordinador(request.user):
        FormClass = ReporteAdminForm
        template = 'app/formulario_admin.html'
    else:
        FormClass = ReporteForm
        template = 'app/formulario.html'

    if request.method == 'POST':
        form = FormClass(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('datatable')
    else:
        form = FormClass()
    return render(request, template, {'form': form})

@login_required
@user_passes_test(is_coordinador, login_url='/acceso-denegado/')
def modificar_reporte(request, pk):
    reporte = Reporte.objects.get(pk=pk)
    if request.method == 'POST':
        form = ReporteAdminForm(request.POST, request.FILES, instance=reporte)
        if form.is_valid():
            # Obtener el personal del formulario
            personal = form.cleaned_data.get('personal')
            if personal in ['Técnico de Cuadrilla', 'Técnico de Infraestructura']:
                # Construir el código de referencia
                year = datetime.now().year % 100 
                referencia = f"GEEI{year:02d}-{reporte.id:04d}"
                # Asignar el código de referencia 
                form.instance.referencia = referencia
            form.save()
            return redirect('datatable')
    else:
        form = ReporteAdminForm(instance=reporte)
    return render(request, 'app/formulario_admin.html', {'form': form, 'objeto': form})