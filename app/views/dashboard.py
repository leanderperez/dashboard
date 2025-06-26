from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app.models import Reporte
from django.http import JsonResponse
from django.template.loader import render_to_string
import pandas as pd
import plotly.graph_objects as go


@login_required
def index(request):
    reportes = Reporte.objects.all()
    df = pd.DataFrame(list(reportes.values()))
        
    context = {
        'clasificaciones': df['clasificacion'].unique(),
        'sucursales_list': df['sucursal'].unique(),
        'personal': df['personal'].unique(),
    }
    return render(request, 'app/dashboard.html', context)

@login_required
def grafico_clasificacion(request):
    reportes = Reporte.objects.all()
    df = pd.DataFrame(list(reportes.values()))
    df['personal'] = df['personal'].replace(['', 'None'], 'En Proceso').fillna('En Proceso')
    template = 'seaborn'

    # Convertir la columna 'fecha' a datetime
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')

    # Filtros
    if request.method == 'POST':
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        clasificacion = request.POST.get('clasificacion')
        sucursales = request.POST.getlist('sucursales')
        personal = request.POST.get('personal')

        if fecha_inicio and fecha_fin:
            df = df[(df['fecha'] >= fecha_inicio) & (df['fecha'] <= fecha_fin)]
        if clasificacion:
            df = df[df['clasificacion'] == clasificacion]
        if sucursales:
            df = df[df['sucursal'].isin(sucursales)]
        if personal:
            df = df[df['personal'] == personal]


    # Gráfico 1: Reportes vs Clasificación (abierto/cerrado)
    grouped = df.groupby(['clasificacion', 'estatus']).size().unstack(fill_value=0)
    fig1 = go.Figure(data=[
        go.Bar(name='Abierto', x=grouped.index, y=grouped.get(False, [0]*len(grouped.index))),
        go.Bar(name='Cerrado', x=grouped.index, y=grouped.get(True, [0]*len(grouped.index)))
    ])
    fig1.update_layout(width=800, 
                       height=250,
                       title="Reportes vs Clasificación",
                       xaxis_title="Clasificación (abierto/cerrado)",
                       yaxis_title="Número de Reportes",
                       template=template,
                       margin=dict(l=10, r=10, t=35, b=5))

    # Gráfico 2: Reportes vs Clasificación (personal)
    grouped = df.groupby(['clasificacion', 'personal']).size().unstack(fill_value=0)
    fig2 = go.Figure(data=[go.Bar(name=col, x=grouped.index, y=grouped[col]) for col in grouped.columns])
    fig2.update_layout(width=800, 
                       height=250,
                       title="Reportes vs Clasificación",
                       xaxis_title="Clasificación (personal)",
                       yaxis_title="Número de Reportes",
                       template=template,
                       margin=dict(l=10, r=10, t=35, b=5))

    html = render_to_string('app/partials/grafico_clasificacion.html', {'fig1': fig1.to_html(), 'fig2': fig2.to_html()})
    return JsonResponse({'html': html})

@login_required
def grafico_sucursales(request):
    reportes = Reporte.objects.all()
    df = pd.DataFrame(list(reportes.values()))
    df['personal'] = df['personal'].replace(['', 'None'], 'En Proceso').fillna('En Proceso')
    template = 'seaborn'

    # Convertir la columna 'fecha' a datetime
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')

    # Filtros
    if request.method == 'POST':
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        clasificacion = request.POST.get('clasificacion')
        sucursales = request.POST.getlist('sucursales')
        personal = request.POST.get('personal')

        if fecha_inicio and fecha_fin:
            df = df[(df['fecha'] >= fecha_inicio) & (df['fecha'] <= fecha_fin)]
        if clasificacion:
            df = df[df['clasificacion'] == clasificacion]
        if sucursales:
            df = df[df['sucursal'].isin(sucursales)]
        if personal:
            df = df[df['personal'] == personal]


    # Gráfico 3: Reportes por Sucursal
    sucursal_counts = df['sucursal'].value_counts()
    fig3 = go.Figure(data=[go.Bar(x=sucursal_counts.index, y=sucursal_counts.values)])
    fig3.update_layout(width=800, 
                       height=250,
                       title="Reportes por Sucursal",
                       xaxis_title="Sucursales",
                       yaxis_title="Número de Reportes",
                       template=template,
                       margin=dict(l=10, r=10, t=35, b=5))

    # Gráfico 4: Reportes por Mes
    monthly_counts = df.groupby(df['fecha'].dt.to_period('M')).size()
    fig4 = go.Figure(data=[go.Scatter(x=monthly_counts.index.astype(str), y=monthly_counts.values, mode='lines+markers')])
    fig4.update_layout(width=800, 
                       height=250,
                       title="Reportes por Mes",
                       xaxis_title="Mes",
                       yaxis_title="Número de Reportes",
                       template=template,
                       margin=dict(l=10, r=10, t=35, b=5))
    
    html = render_to_string('app/partials/grafico_sucursales.html', {'fig3': fig3.to_html(), 'fig4': fig4.to_html()})
    return JsonResponse({'html': html})

@login_required
def grafico_kilos(request):
    reportes = Reporte.objects.all()
    df = pd.DataFrame(list(reportes.values()))
    df['personal'] = df['personal'].replace(['', 'None'], 'En Proceso').fillna('En Proceso')
    template = 'seaborn'

    # Convertir la columna 'fecha' a datetime
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')

    # Filtros
    if request.method == 'POST':
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        clasificacion = request.POST.get('clasificacion')
        sucursales = request.POST.getlist('sucursales')
        personal = request.POST.get('personal')

        if fecha_inicio and fecha_fin:
            df = df[(df['fecha'] >= fecha_inicio) & (df['fecha'] <= fecha_fin)]
        if clasificacion:
            df = df[df['clasificacion'] == clasificacion]
        if sucursales:
            df = df[df['sucursal'].isin(sucursales)]
        if personal:
            df = df[df['personal'] == personal]


    # Gráfico 5: Kilos de Refrigerante Recargados por Sucursal
    fig5 = go.Figure()
    for refrigerante in df['refrigerante'].unique():
        if refrigerante:
            refrigerante_data = df[df['refrigerante'] == refrigerante]
            sucursal_kilos = refrigerante_data.groupby('sucursal')['kilos'].sum()
            fig5.add_trace(go.Bar(x=sucursal_kilos.index, y=sucursal_kilos.values, name=refrigerante))
    fig5.update_layout(width=800, 
                    height=250,
                    title="Kilos de Refrigerante Recargados por Sucursal",
                    xaxis_title="Sucursales",
                    yaxis_title="Refrigerante (Kg)",
                    template=template,
                    margin=dict(l=10, r=10, t=35, b=5))

    # Gráfico 6: Kilos de Refrigerante por Mes
    fig6 = go.Figure()
    for refrigerante in df['refrigerante'].unique():
        if refrigerante:
            monthly_kilos = df[df['refrigerante'] == refrigerante].groupby(df['fecha'].dt.to_period('M'))['kilos'].sum()
            fig6.add_trace(go.Scatter(x=monthly_kilos.index.astype(str), y=monthly_kilos.values, mode='lines+markers', name=refrigerante))
    fig6.update_layout(width=800, 
                    height=250,
                    title="Kilos de Refrigerante Recargados por Mes",
                    xaxis_title="Mes",
                    yaxis_title="Refrigerante (Kg)",
                    template=template,
                    margin=dict(l=10, r=10, t=35, b=5))
    
    html = render_to_string('app/partials/grafico_kilos.html', {'fig5': fig5.to_html(), 'fig6': fig6.to_html()})
    return JsonResponse({'html': html})

@login_required
def grafico_costos(request):
    reportes = Reporte.objects.all()
    df = pd.DataFrame(list(reportes.values()))
    df['personal'] = df['personal'].replace(['', 'None'], 'En Proceso').fillna('En Proceso')
    template = 'seaborn'

    # Convertir la columna 'fecha' a datetime
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')

    # Filtros
    if request.method == 'POST':
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        clasificacion = request.POST.get('clasificacion')
        sucursales = request.POST.getlist('sucursales')
        personal = request.POST.get('personal')

        if fecha_inicio and fecha_fin:
            df = df[(df['fecha'] >= fecha_inicio) & (df['fecha'] <= fecha_fin)]
        if clasificacion:
            df = df[df['clasificacion'] == clasificacion]
        if sucursales:
            df = df[df['sucursal'].isin(sucursales)]
        if personal:
            df = df[df['personal'] == personal]


    # Grafico 7: Comparativo de Costos - Forum GEEI vs Contratista
    df = df[df['personal'] != 'En Proceso']
    df['personal'] = df['personal'].replace({'Técnico de Cuadrilla': 'Forum GEEI', 'Técnico de Infraestructura': 'Forum GEEI'})

    df_costos = df[df['personal'].isin(['Forum GEEI', 'Contratista'])]
    df_agrupado = df_costos.groupby('personal').agg({'costo': 'sum', 'gasto': 'sum'}).reset_index()
    df_agrupado['ahorro'] = df_agrupado['costo'] - df_agrupado['gasto']

    fig7 = go.Figure(
        data=[
            # Barra de referencia: Costo (paralela)
            go.Bar(
                x=df_agrupado['costo'],
                y=df_agrupado['personal'],
                name='Costo',
                orientation='h',
                text=df_agrupado['costo'].apply(lambda a: f'Costo: {a} $'),
                textposition='auto',
                offsetgroup='costo',  # Grupo separado
                width=0.3
            ),
            # Gasto (apilado)
            go.Bar(
                x=df_agrupado['gasto'],
                y=df_agrupado['personal'],
                name='Gasto',
                orientation='h',
                text=df_agrupado['gasto'].apply(lambda a: f'Gasto: {a} $'),
                textposition='auto',
                offsetgroup='ga',  # Grupo para apilar gasto+ahorro
                width=0.3
            ),
            # Ahorro (apilado sobre Gasto)
            go.Bar(
                x=df_agrupado['ahorro'],
                y=df_agrupado['personal'],
                name='Ahorro',
                orientation='h',
                text=df_agrupado['ahorro'].apply(lambda a: f'Ahorro: {a} $'),
                textposition='auto',
                offsetgroup='ga',
                base=df_agrupado['gasto'],  # Apilar sobre gasto
                width=0.3
            )
        ]
    )
    fig7.update_layout(
        width=800,
        height=250,
        title="Comparativo de Costo, Gasto y Ahorro - GEEI vs Contratista",
        barmode='relative', 
        xaxis_title="Monto ($)",
        yaxis_title="Personal",
        template=template,
        margin=dict(l=10, r=10, t=35, b=5)
    )

    # Grafico 8: Comparativo de Costos - Forum GEEI vs Contratista
    df_gastos = df[df['personal'].isin(['Forum GEEI', 'Contratista'])]

    # Agrupa por mes y personal, sumando gasto y costo
    df_gastos['mes'] = df_gastos['fecha'].dt.to_period('M').astype(str)
    gastos_mensuales = df_gastos.groupby(['mes', 'personal'])[['gasto', 'costo']].sum().reset_index()
    gastos_mensuales['ahorro'] = gastos_mensuales['costo'] - gastos_mensuales['gasto']

    fig8 = go.Figure()

    for personal in ['Forum GEEI', 'Contratista']:
        datos = gastos_mensuales[gastos_mensuales['personal'] == personal]
        # Línea de gasto
        fig8.add_trace(go.Scatter(
            x=datos['mes'],
            y=datos['gasto'],
            mode='lines+markers',
            name=f'Gasto {personal}'
        ))
        # Línea de ahorro
        fig8.add_trace(go.Scatter(
            x=datos['mes'],
            y=datos['ahorro'],
            mode='lines+markers',
            name=f'Ahorro {personal}',
            line=dict(dash='dash')  # Línea punteada para distinguir el ahorro
        ))

    fig8.update_layout(
        width=800,
        height=250,
        title="Gastos y Ahorro Mensual por Contratista y Forum GEEI",
        xaxis_title="Mes",
        yaxis_title="Monto ($)",
        template=template,
        margin=dict(l=10, r=10, t=35, b=5)
    )
        
    html = render_to_string('app/partials/grafico_costos.html', {'fig7': fig7.to_html(), 'fig8': fig8.to_html()})
    return JsonResponse({'html': html})