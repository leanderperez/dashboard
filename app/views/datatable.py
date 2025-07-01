from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app.models import Reporte


@login_required
def datatable(request):
    user = request.user
    if user.groups.filter(name='Supervisores').exists():
        sucursal = user.perfil.sucursal
        reportes = Reporte.objects.filter(sucursal=sucursal)
    else:
        reportes = Reporte.objects.all()
    contexto = {'reportes': reportes}
    return render(request, 'app/datatable.html', contexto)