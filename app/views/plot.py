from django.shortcuts import render
import plotly.graph_objects as go
from plotly.offline import plot

def generar_grafico(temperaturas, horas, setpoint, equipo):
    # Crear el gráfico
    fig = go.Figure()

    # Área sombreada
    fig.add_trace(go.Scatter(x=horas + horas[::-1],
                             y=[setpoint - 2] * len(horas) + [setpoint + 2] * len(horas),
                             fill="toself", fillcolor="lightgreen", opacity=0.4,
                             line=dict(color="lightgray", width=0),
                             hoverinfo="none",
                             name="Rango de operación",
                             showlegend=False))

    # Datos de temperatura
    fig.add_trace(go.Scatter(x=horas, y=temperaturas, mode='lines+markers+text', name='Temperatura', text=[f'{temp}' for temp in temperaturas],
                             textposition='top center', line=dict(color='orange')))

    # Línea de setpoint
    fig.add_trace(go.Scatter(x=horas, y=[setpoint] * len(horas), mode='lines', name='Setpoint', hoverinfo="none", line=dict(color='green', dash='dash')))


    # Layout del gráfico
    fig.update_layout(title=f'Variación de Temperaturas<Br>{equipo}',
                      xaxis_title='Hora',
                      yaxis_title='Temperatura (°C)',
                      yaxis_range=[setpoint - 6, setpoint + 6],
                      template='plotly',
                      legend=dict(
                          x=0.70,
                          y=1.00,
                          bgcolor='rgba(255, 255, 255, 0.5)',
                          bordercolor='gray'),
                          margin=dict(
                            l=25,  # Margen izquierdo
                            r=25,  # Margen derecho
                            b=50, # Margen inferior
                            t=75,  # Margen superior
                            pad=4))

    # Convertir el gráfico a HTML
    plot_div = plot(fig, output_type='div')

    return plot_div

def crear_plot(request):
    if request.method == 'POST':
        temperaturas = [float(t) for t in request.POST['temperaturas'].split(',')]
        horas = [str(h) for h in request.POST['horas'].split(',')]
        setpoint = float(request.POST['setpoint'])
        equipo = str(request.POST['equipo'])

        plot_div = generar_grafico(temperaturas, horas, setpoint, equipo)
        return render(request, 'app/plot.html', {'plot_div': plot_div})

    return render(request, 'app/plot.html')