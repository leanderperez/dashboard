from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app.models import Reporte



def pendientes(request):
    reportes = Reporte.objects.all()
    contexto = {'reportes': reportes}
    return render(request, 'app/pendientes.html', contexto)