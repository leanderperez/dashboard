from django.shortcuts import render
from django.contrib.auth.decorators import login_required
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

@login_required
def index(request):
    reportes = Reporte.objects.all()  # Obtiene todos los reportes
    plot_div1 = generar_grafico(reportes)  # Genera el primer gráfico
    plot_div2 = generar_grafico(reportes)  # Genera el segundo gráfico
    plot_div3 = generar_grafico(reportes)  # Genera el tercer gráfico
    plot_div4 = generar_grafico(reportes)  # Genera el cuarto gráfico
    return render(request, 'app/dashboard.html', {'plot_div1': plot_div1, 'plot_div2': plot_div2, 'plot_div3': plot_div3, 'plot_div4': plot_div4})

def actualizar_grafico(request):
    if request.method == 'POST':
        sucursales = request.POST.getlist('sucursal[]')  # Obtiene la lista de sucursales seleccionadas
        reportes = Reporte.objects.all()
        if sucursales:
            reportes = reportes.filter(sucursal__in=sucursales)
        plot_div = generar_grafico(reportes)
        return JsonResponse({'plot_div': plot_div})
    return JsonResponse({'error': 'No se proporcionaron sucursales'})