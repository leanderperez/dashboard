from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from app.models import Material, SolicitudMaterial, DetalleSolicitud
from django.contrib.auth.decorators import login_required, user_passes_test
from app.forms.forms import MaterialForm, SolicitudMaterialForm, DetalleSolicitudFormSet
import json
from django.core.mail import send_mail, EmailMessage
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.contrib.admin.views.decorators import staff_member_required

def es_supervisor(user):
    return user.is_superuser  # O verifica un grupo específico, como user.groups.filter(name='Supervisores').exists()

@login_required
def lista_materiales(request):
    materiales = Material.objects.all()
    sucursales = SolicitudMaterialForm.base_fields['sucursal'].choices  # Obtener las opciones de SUCURSALES
    return render(request, 'requisiciones/lista_materiales.html', {
        'materiales': materiales,
        'sucursales': sucursales
    })

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

@login_required
def crear_solicitud_material(request):
    if request.method == 'POST':
        materiales_data = json.loads(request.POST.get('materiales', '[]'))
        sucursal = request.POST.get('sucursal')
        observaciones = request.POST.get('observaciones')

        # Crear la solicitud de materiales
        solicitud = SolicitudMaterial.objects.create(
            usuario=request.user,
            sucursal=sucursal,
            observaciones=observaciones
        )

        # Agregar los materiales seleccionados a la solicitud
        for material_data in materiales_data:
            material = Material.objects.get(pk=material_data['id'])
            DetalleSolicitud.objects.create(
                solicitud=solicitud,
                material=material,
                cantidad=material_data['cantidad']
            )

        # Enviar correo al supervisor
        enviar_correo_aprobacion(request, solicitud, 'leperez@forum.com.ve')

        return JsonResponse({'message': 'Solicitud creada exitosamente.'})
    return JsonResponse({'error': 'Método no permitido.'}, status=405)


def aprobar_solicitud(request, token):
    solicitud = get_object_or_404(SolicitudMaterial, token=token)
    solicitud.aprobada = True
    solicitud.save()
    return HttpResponse("La solicitud ha sido aprobada exitosamente.")

def enviar_correo_aprobacion(request, solicitud, supervisor_email):
    aprobar_url = reverse('aprobar_solicitud', args=[solicitud.token])
    aprobar_url = f"{request.build_absolute_uri(aprobar_url)}"

    # Obtener los materiales relacionados con la solicitud
    detalles = solicitud.detallesolicitud_set.all()

    # Construir la tabla de materiales
    materiales_html = "<table border='1' style='border-collapse: collapse; width: 100%;'>"
    materiales_html += "<tr><th>Material</th><th>Cantidad</th><th>Unidad de Medida</th></tr>"
    for detalle in detalles:
        materiales_html += f"""
        <tr>
            <td>{detalle.material.nombre}</td>
            <td>{detalle.cantidad}</td>
            <td>{detalle.material.unidad_medida}</td>
        </tr>
        """
    materiales_html += "</table>"

    # Construir el mensaje del correo
    mensaje_html = f"""
    <html>
    <body>
        <p>Se ha generado una nueva solicitud de materiales.</p>
        <p><strong>Sucursal:</strong> {solicitud.sucursal}</p>
        <p><strong>Observaciones:</strong> {solicitud.observaciones}</p>
        <p><strong>Materiales solicitados:</strong></p>
        {materiales_html}
        <p>
            <a href="{aprobar_url}" style="padding: 10px 20px; color: white; background-color: green; text-decoration: none; border-radius: 5px;">Aprobar Solicitud</a>
        </p>
    </body>
    </html>
    """

    # Enviar el correo
    email = EmailMessage(
        subject= f"Solicitud #{solicitud.id} - {solicitud.fecha_solicitud} - {solicitud.sucursal}",
        body=mensaje_html,
        from_email='leanderperez@gmail.com',
        to=[supervisor_email]
    )
    email.content_subtype = 'html'  # Indicar que el contenido es HTML
    email.send()