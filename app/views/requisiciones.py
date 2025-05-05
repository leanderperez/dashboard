from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from app.models import Material, SolicitudMaterial, DetalleSolicitud
from django.contrib.auth.decorators import login_required
import json
from django.core.mail import EmailMessage
from django.urls import reverse
from django.conf import settings

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from io import BytesIO
from django.views.decorators.csrf import csrf_exempt


@login_required
def lista_solicitudes(request):
    solicitudes = SolicitudMaterial.objects.all()
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

    # Ruta del logo
    logo_path = f"{settings.BASE_DIR}/app/static/images/logo.png"

    # Dibujar el logo en el encabezado
    pdf.drawImage(logo_path, 50, 710, width=100, height=50, preserveAspectRatio=True, mask='auto')

    # Encabezado
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(200, 730, f"  Solicitud de Materiales #{solicitud.id}")
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(500, 730, f"{solicitud.fecha_solicitud}")
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(60, 680, f"{solicitud.sucursal}")
    pdf.setFont("Helvetica", 10)
    pdf.drawString(60, 665, f"Solicitante: {solicitud.usuario.username}")
    pdf.drawString(60, 650, "Aprobada: ")
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(110, 650, "Sí" if solicitud.estado == 'aprobada' else "No")
    pdf.setFont("Helvetica", 10)
    pdf.drawString(130, 650, f"Completada: ")
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(190, 650, "Sí" if solicitud.completado else "No")
    pdf.setFont("Helvetica", 10)
    pdf.drawString(60, 635, f"Observaciones: {solicitud.observaciones or 'N/A'}")

    # Espacio para la tabla
    pdf.drawString(60, 590, "Detalles de los materiales:")

    # Crear la tabla de materiales con texto ajustable
    styles = getSampleStyleSheet()
    style_normal = styles['Normal']

    data = [["Material", "Cantidad", "Unidad de Medida"]]
    for detalle in detalles:
        material_paragraph = Paragraph(detalle.material.nombre, style_normal)
        data.append([material_paragraph, detalle.cantidad, detalle.material.unidad_medida])

    # Configurar la tabla con anchos fijos
    col_widths = [250, 100, 150]  # Anchos fijos para las columnas
    table = Table(data, colWidths=col_widths)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Fondo de la fila del encabezado
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Color del texto del encabezado
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Centrar horizontalmente
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Centrar verticalmente
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fuente del encabezado
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Espaciado inferior en el encabezado
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),  # Línea debajo del encabezado
        ('LINEBELOW', (0, 1), (-1, -1), 0.5, colors.black),  # Líneas horizontales entre las filas
    ]))

    # Dibujar la tabla en el PDF
    table.wrapOn(pdf, 50, 570)
    table.drawOn(pdf, 50, 570 - len(data) * 20)

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

        # Enviar correo a los supervisores
        supervisor_emails = ['serv.grales.gerencia@forum.com.ve', 'serv.grales.subgerencia@forum.com.ve']
        enviar_correo_aprobacion(request, solicitud, supervisor_emails)

        return JsonResponse({'message': 'Solicitud creada exitosamente.'})
    return JsonResponse({'error': 'Método no permitido.'}, status=405)

def enviar_correo_aprobacion(request, solicitud, supervisor_emails):
    aprobar_url = reverse('cambiar_estado_solicitud', args=[solicitud.token, 'aprobar'])
    rechazar_url = reverse('cambiar_estado_solicitud', args=[solicitud.token, 'rechazar'])
    aprobar_url = f"{request.build_absolute_uri(aprobar_url)}"
    rechazar_url = f"{request.build_absolute_uri(rechazar_url)}"

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
            <a href="{rechazar_url}" style="padding: 10px 20px; color: white; background-color: red; text-decoration: none; border-radius: 5px;">Rechazar Solicitud</a>
        </p>
    </body>
    </html>
    """

    # Enviar el correo
    email = EmailMessage(
        subject=f"Solicitud #{solicitud.id} - {solicitud.fecha_solicitud} - {solicitud.sucursal}",
        body=mensaje_html,
        from_email='leanderperez@gmail.com',
        to=supervisor_emails  # Lista de correos electrónicos
    )
    email.content_subtype = 'html'  # Indicar que el contenido es HTML
    email.send()

def cambiar_estado_solicitud(request, token, accion):
    solicitud = get_object_or_404(SolicitudMaterial, token=token)
    if accion == 'aprobar':
        solicitud.estado = 'aprobada'
    elif accion == 'rechazar':
        solicitud.estado = 'rechazada'
    else:
        return HttpResponse("Acción no válida.", status=400)
    solicitud.save()
    return HttpResponse(f"La solicitud ha sido {solicitud.get_estado_display()} exitosamente.")

@csrf_exempt
@login_required
def completar_solicitud(request, pk):
    if request.method == 'POST':
        solicitud = get_object_or_404(SolicitudMaterial, pk=pk)
        solicitud.completado = True
        solicitud.save()
        return JsonResponse({'message': 'Solicitud completada exitosamente.'})
    return JsonResponse({'error': 'Método no permitido.'}, status=405)

@csrf_exempt
@login_required
def asignar_analista(request, pk):
    if request.method == 'POST':
        solicitud = get_object_or_404(SolicitudMaterial, pk=pk)
        data = json.loads(request.body)
        analista = data.get('analista')
        if analista in ['Cesar B.', 'José A.']:
            solicitud.analista = analista
            solicitud.save()
            return JsonResponse({'message': 'Analista asignado exitosamente.'})
        return JsonResponse({'error': 'Analista no válido.'}, status=400)
    return JsonResponse({'error': 'Método no permitido.'}, status=405)