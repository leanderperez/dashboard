from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from app.models import Material, SolicitudMaterial, DetalleSolicitud
from django.contrib.auth.decorators import login_required, user_passes_test
from app.forms.forms import MaterialForm, SolicitudMaterialForm, DetalleSolicitudFormSet
import json
from django.core.mail import send_mail, EmailMessage
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from io import BytesIO

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
    # Obtener la solicitud
    solicitud = get_object_or_404(SolicitudMaterial, pk=pk)
    detalles = solicitud.detallesolicitud_set.all()

    # Crear un buffer para el PDF
    buffer = BytesIO()

    # Crear el canvas de ReportLab
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setTitle(f"Solicitud #{solicitud.id}")

    # Encabezado
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, 750, f"Solicitud de Materiales #{solicitud.id}")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, 730, f"Usuario: {solicitud.usuario.username}")
    pdf.drawString(50, 710, f"Fecha: {solicitud.fecha_solicitud}")
    pdf.drawString(50, 690, f"Sucursal: {solicitud.sucursal}")
    pdf.drawString(50, 670, f"Observaciones: {solicitud.observaciones or 'N/A'}")
    pdf.drawString(50, 650, f"Aprobada: {'Sí' if solicitud.aprobada else 'No'}")
    pdf.drawString(50, 630, f"Completada: {'Sí' if solicitud.completado else 'No'}")

    # Espacio para la tabla
    pdf.drawString(100, 575, "Detalles de los materiales:")

    # Crear la tabla de materiales con texto ajustable
    styles = getSampleStyleSheet()
    style_normal = styles['Normal']

    data = [["Material", "Cantidad", "Unidad de Medida"]]
    for detalle in detalles:
        material_paragraph = Paragraph(detalle.material.nombre, style_normal)
        data.append([material_paragraph, detalle.cantidad, detalle.material.unidad_medida])

    # Configurar la tabla con anchos fijos
    col_widths = [200, 100, 150]  # Anchos fijos para las columnas
    table = Table(data, colWidths=col_widths)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.ReportLabBluePCMYK),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Dibujar la tabla en el PDF
    table.wrapOn(pdf, 75, 550)
    table.drawOn(pdf, 75, 550 - len(data) * 20)

    # Finalizar el PDF
    pdf.save()

    # Enviar el PDF como respuesta HTTP
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="Solicitud_{solicitud.id}.pdf"'
    return response

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
        <p><strong>Usuario:</strong> {solicitud.usuario.username}</p>
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