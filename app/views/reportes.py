from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app.forms.forms import ReporteForm, ReporteAdminForm
from app.models import Reporte

@login_required
def crear_reporte(request):
    if request.method == 'POST':
        form = ReporteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('datatable')  # Redirige a datatable
    else:
        form = ReporteForm()
    return render(request, 'app/formulario.html', {'form': form})

@login_required
def modificar_reporte(request, pk):
    form = Reporte.objects.get(pk=pk)
    if request.method == 'POST':
        form = ReporteAdminForm(request.POST, request.FILES, instance=form)
        if form.is_valid():
            form.save()
            return redirect('datatable')  # Redirige a datatable
    else:
        form = ReporteAdminForm(instance=form)
    return render(request, 'app/formulario_admin.html', {'form': form, 'objeto': form})
