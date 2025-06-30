from django.shortcuts import render, redirect, get_object_or_404
from app.models import Material
from django.contrib.auth.decorators import login_required, user_passes_test
from app.forms.forms import MaterialForm, SolicitudMaterialForm
from django.contrib.admin.views.decorators import staff_member_required
from app.views.login import is_coordinador

@login_required
@user_passes_test(is_coordinador, login_url='/acceso-denegado/')
def lista_materiales(request):
    materiales = Material.objects.all()
    sucursales = SolicitudMaterialForm.base_fields['sucursal'].choices  # Obtener las opciones de SUCURSALES
    return render(request, 'requisiciones/lista_materiales.html', {
        'materiales': materiales,
        'sucursales': sucursales
    })

@staff_member_required
def crear_material(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_materiales')
    else:
        form = MaterialForm()
    return render(request, 'requisiciones/crear_material.html', {'form': form})

@staff_member_required
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

@staff_member_required
def eliminar_material(request, pk):
    material = get_object_or_404(Material, pk=pk)
    if request.method == 'POST':
        material.delete()
        return redirect('lista_materiales')
    return render(request, 'requisiciones/eliminar_material.html', {'material': material})