from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app.forms.forms import ReporteForm, ReporteAdminForm
from app.models import Reporte
from datetime import datetime

@login_required
def crear_reporte(request):
    if request.method == 'POST':
        form = ReporteAdminForm(request.POST)
        if form.is_valid():
            form.save()  # Guardar el objeto primero para obtener el ID
            if form.instance.personal in ['Técnico de Cuadrilla', 'Técnico de Infraestructura']:
                # Construir el código de referencia
                year = datetime.now().year % 100
                referencia = f"GEEI{year:02d}-{form.instance.id:04d}"
                form.instance.referencia = referencia
                form.instance.save()  # Guardar nuevamente para actualizar el campo referencia
            elif not form.instance.referencia:
                form.instance.referencia = '⚠️ Nuevo'
                form.instance.save()  # Guardar nuevamente para actualizar el campo referencia
            return redirect('datatable')  # Redirige a datatable
    else:
        form = ReporteAdminForm()
    return render(request, 'app/formulario_admin.html', {'form': form})

@login_required
def modificar_reporte(request, pk):
    reporte = Reporte.objects.get(pk=pk)
    if request.method == 'POST':
        form = ReporteAdminForm(request.POST, request.FILES, instance=reporte)
         
        if form.is_valid():
            # Obtener el personal del formulario
            personal = form.cleaned_data.get('personal')
            if personal in ['Técnico de Cuadrilla', 'Técnico de Infraestructura']:
                # Construir el código de referencia
                year = datetime.now().year % 100  # Obtener los dos últimos dígitos del año en curso
                referencia = f"GEEI{year:02d}-{reporte.id:04d}"
                # Asignar el código de referencia al campo correspondiente
                form.instance.referencia = referencia
            form.save()
            return redirect('datatable')  # Redirige a datatable
    else:
        form = ReporteAdminForm(instance=reporte)
    return render(request, 'app/formulario_admin.html', {'form': form, 'objeto': form})