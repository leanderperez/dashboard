from django.shortcuts import render, redirect
from app.forms import ReporteForm, ReporteAdminForm
from app.models import Reporte

def crear_reporte(request):
    if request.method == 'POST':
        form = ReporteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('datatable_reportes')  # Redirige a una página de éxito
    else:
        form = ReporteForm()
    return render(request, 'app/formulario.html', {'form': form})

def modificar_reporte(request, pk):
    form = Reporte.objects.get(pk=pk)
    if request.method == 'POST':
        form = ReporteAdminForm(request.POST, instance=form)
        if form.is_valid():
            form.save()
            return redirect('datatable_reportes')  # Redirige a una página de éxito
    else:
        form = ReporteAdminForm(instance=form)
    return render(request, 'app/formulario_admin.html', {'form': form, 'objeto': form})
