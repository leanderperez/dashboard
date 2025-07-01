from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app.models import Reporte


@login_required
def pendientes(request):
    user = request.user
    if user.groups.filter(name='Supervisores').exists():
        sucursal = user.perfil.sucursal
        reportes = Reporte.objects.filter(sucursal=sucursal, estatus=False)
        contexto = {'reportes': reportes}
    else:
        coordinador = request.user.username
        reportes = Reporte.objects.filter(estatus=False, coordinador=coordinador)
        contexto = {'reportes': reportes,
                'coordinador': coordinador}
    return render(request, 'app/pendientes.html', contexto)