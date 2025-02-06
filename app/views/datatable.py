from django.shortcuts import render
from app.models import Reporte

def datatable_reportes(request):
    reportes = Reporte.objects.all()
    contexto = {'reportes': reportes}
    return render(request, 'app/datatable_reportes.html', contexto)