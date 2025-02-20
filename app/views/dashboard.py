from django.shortcuts import render
from app.models import Reporte
import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot
from django.http import JsonResponse

def generar_grafico(queryset):
    df = pd.DataFrame(list(queryset.values('sucursal')))
    df = df['sucursal'].value_counts()
    fig = go.Figure(data=[go.Bar(x=df.index, y=df.values)])
    fig.update_layout(title='Gráfico de Reportes por Sucursal')
    plot_div = plot(fig, output_type='div')
    return plot_div

def index(request):
    reportes = Reporte.objects.all()  # Obtiene todos los reportes
    sucursales = Reporte.objects.values_list('sucursal', flat=True).distinct()
    plot_div = generar_grafico(reportes)  # Genera el gráfico
    if request.method == 'GET':  # Maneja la solicitud GET inicial
        return render(request, 'app/dashboard.html', {'sucursales': sucursales, 'plot_div': plot_div})
    elif request.method == 'POST':  # Maneja la solicitud POST de AJAX
        return actualizar_grafico(request)  # Llama a la vista actualizar_grafico

def actualizar_grafico(request):
    if request.method == 'POST':
        sucursales = request.POST.getlist('sucursal[]')  # Obtiene la lista de sucursales seleccionadas
        reportes = Reporte.objects.all()
        if sucursales:
            reportes = reportes.filter(sucursal__in=sucursales)
        plot_div = generar_grafico(reportes)
        return JsonResponse({'plot_div': plot_div})
    return JsonResponse({'error': 'No se proporcionaron sucursales'})