from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app.models import Reporte
import pandas as pd
import plotly.graph_objects as go

@login_required
def index(request):
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
    
    # Grafico 7 y 8: Costos por Personal
    df = df[df['personal'] != 'En Proceso']
    df['personal'] = df['personal'].replace({'Técnico de Cuadrilla': 'Forum GEEI', 'Técnico de Infraestructura': 'Forum GEEI'})

    # Grafico 7: Filtrar datos para Forum GEEI
    df_forum = df[df['personal'] == 'Forum GEEI']
    df_agrupado_forum = df_forum.groupby('personal').agg({'costo': 'sum', 'gasto': 'sum'}).reset_index()
    df_agrupado_forum['ahorro'] = df_agrupado_forum['costo'] - df_agrupado_forum['gasto']
    fig7 = go.Figure(
        data=[
            go.Bar(
                x=df_agrupado_forum['costo'],
                y=df_agrupado_forum['personal'],
                name='Costo',
                orientation='h',
                text=df_agrupado_forum['costo'].apply(lambda a: f'Costo: {a} $')
            ),
            go.Bar(
                x=df_agrupado_forum['gasto'],
                y=df_agrupado_forum['personal'],
                name='Gasto',
                orientation='h',
                text=df_agrupado_forum['gasto'].apply(lambda a: f'Gasto: {a} $')
            ),
            go.Bar(
                x=df_agrupado_forum['ahorro'],
                y=df_agrupado_forum['personal'],
                name='Ahorro',
                orientation='h',
                base=df_agrupado_forum['gasto'],  # Ajustar la base para que comience donde termina la barra de gasto
                marker={'color': 'lightgreen'},
                text=df_agrupado_forum['ahorro'].apply(lambda a: f'Ahorro: {a} $'),
                textposition='auto'
            )
        ],
    )
    fig7.update_layout(width=800, 
                    height=250,
                    title="Grafico de costos - Forum GEEI",
                    barmode='group',
                    xaxis_title="Costo",
                    yaxis_title="Personal",
                    template=template,
                    margin=dict(l=10, r=10, t=35, b=5))

    # Grafico 8: Filtrar datos para Contratista
    df_contratista = df[df['personal'] == 'Contratista']
    df_agrupado_contratista = df_contratista.groupby('personal').agg({'costo': 'sum', 'gasto': 'sum'}).reset_index()
    df_agrupado_contratista['ahorro'] = df_agrupado_contratista['costo'] - df_agrupado_contratista['gasto']
    fig8 = go.Figure(
        data=[
            go.Bar(
                x=df_agrupado_contratista['costo'],
                y=df_agrupado_contratista['personal'],
                name='Costo',
                orientation='h',
                text=df_agrupado_contratista['costo'].apply(lambda a: f'Costo: {a} $')
            ),
            go.Bar(
                x=df_agrupado_contratista['gasto'],
                y=df_agrupado_contratista['personal'],
                name='Gasto',
                orientation='h',
                text=df_agrupado_contratista['gasto'].apply(lambda a: f'Gasto: {a} $')
            ),
            go.Bar(
                x=df_agrupado_contratista['ahorro'],
                y=df_agrupado_contratista['personal'],
                name='Ahorro',
                orientation='h',
                base=df_agrupado_contratista['gasto'], 
                marker={'color': 'lightgreen'},
                text=df_agrupado_contratista['ahorro'].apply(lambda a: f'Ahorro: {a} $'),
                textposition='auto'
            )
        ],
    )
    fig8.update_layout(width=800, 
                    height=250,
                    title="Grafico de costos - Contratista",
                    barmode='group',
                    xaxis_title="Costo",
                    yaxis_title="Personal",
                    template=template,
                    margin=dict(l=10, r=10, t=35, b=5))


        
    context = {
        'fig1': fig1.to_html(),
        'fig2': fig2.to_html(),
        'fig3': fig3.to_html(),
        'fig4': fig4.to_html(),
        'fig5': fig5.to_html(),
        'fig6': fig6.to_html(),
        'fig7': fig7.to_html(),
        'fig8': fig8.to_html(),
        'clasificaciones': df['clasificacion'].unique(),
        'sucursales_list': df['sucursal'].unique(),
        'personal': df['personal'].unique(),
    }
    return render(request, 'app/dashboard.html', context)