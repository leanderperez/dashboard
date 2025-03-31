from django.shortcuts import render, redirect, get_object_or_404
from app.models import Material, SolicitudMaterial, DetalleSolicitud
from django.contrib.auth.decorators import login_required
from app.forms.forms import MaterialForm, SolicitudMaterialForm, DetalleSolicitudFormSet

@login_required
def lista_materiales(request):
    materiales = Material.objects.all()
    return render(request, 'requisiciones/lista_materiales.html', {'materiales': materiales})

@login_required
def crear_material(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_materiales')
    else:
        form = MaterialForm()
    return render(request, 'requisiciones/crear_material.html', {'form': form})

@login_required
def editar_material(request, pk):
    material = get_object_or_404(Material, pk=pk)
    if request.method == 'POST':
        form = MaterialForm(request.POST, instance=material)
        if form.is_valid():
            form.save()
            return redirect('lista_materiales')
    else:
        form = MaterialForm(instance=material)
    return render(request, 'requisiciones/editar_material.html', {'form': form})

@login_required
def eliminar_material(request, pk):
    material = get_object_or_404(Material, pk=pk)
    if request.method == 'POST':
        material.delete()
        return redirect('lista_materiales')
    return render(request, 'requisiciones/eliminar_material.html', {'material': material})

@login_required
def crear_solicitud(request):
    if request.method == 'POST':
        form = SolicitudMaterialForm(request.POST)
        formset = DetalleSolicitudFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            solicitud = form.save(commit=False)
            solicitud.usuario = request.user
            solicitud.save()
            formset.instance = solicitud
            formset.save()
            return redirect('lista_solicitudes')
    else:
        form = SolicitudMaterialForm()
        formset = DetalleSolicitudFormSet()
    return render(request, 'requisiciones/crear_solicitud.html', {'form': form, 'formset': formset})

@login_required
def lista_solicitudes(request):
    solicitudes = SolicitudMaterial.objects.filter(usuario=request.user)
    return render(request, 'requisiciones/lista_solicitudes.html', {'solicitudes': solicitudes})

@login_required
def detalle_solicitud(request, pk):
    solicitud = get_object_or_404(SolicitudMaterial, pk=pk)
    if request.method == 'POST':
        completado = request.POST.get('completado', 'off') == 'on'
        solicitud.completado = completado
        solicitud.save()
        return redirect('detalle_solicitud', pk=pk)
    return render(request, 'requisiciones/detalle_solicitud.html', {'solicitud': solicitud})