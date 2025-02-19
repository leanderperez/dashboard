from django.shortcuts import render
from app.models import Reporte
import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot
from django.http import JsonResponse

def generar_grafico(queryset):
    df = pd.DataFrame(list(queryset.values('coordinador', 'precio')))
    fig = go.Figure(data=[go.Bar(x=df['coordinador'], y=df['precio'])])
    fig.update_layout(title='Gráfico de Productos por Categoría')
    plot_div = plot(fig, output_type='div')
    return plot_div

def index(request):
    productos = Reporte.objects.all()  # Obtiene todos los productos
    categorias = Reporte.objects.values_list('categoria', flat=True).distinct()
    plot_div = generar_grafico(productos)  # Genera el gráfico con todos los productos
    if request.method == 'GET':  # Maneja la solicitud GET inicial
        return render(request, 'index.html', {'categorias': categorias, 'plot_div': plot_div})
    elif request.method == 'POST':  # Maneja la solicitud POST de AJAX
        return actualizar_grafico(request)  # Llama a la vista actualizar_grafico

def actualizar_grafico(request):
    if request.method == 'POST':
        categoria = request.POST.get('coordinador')  # Obtiene la categoría de POST
        productos = Reporte.objects.all()
        if categoria:
            productos = productos.filter(categoria=categoria)
        plot_div = generar_grafico(productos)
        return JsonResponse({'plot_div': plot_div})
    return JsonResponse({'error': 'No se proporcionó la categoría'})