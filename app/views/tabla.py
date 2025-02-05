from django.shortcuts import render
from django.core.paginator import Paginator
from app.models import Reporte

def tabla_reportes(request):
    reportes = Reporte.objects.all()

    # Paginación
    paginator = Paginator(reportes, 10)  # Mostrar 10 productos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Filtros
    sucursal = request.GET.get('sucursal')
    if sucursal:
        reportes = Reporte.objects.filter(sucursal=sucursal)
    else:
        reportes = Reporte.objects.all()

    # Búsqueda
    buscar = request.GET.get('buscar')
    if buscar:
        reportes = reportes.filter(reporte__icontains=buscar)  # Búsqueda insensible a mayúsculas

    context = {
        'page_obj': page_obj,
        'sucursales': Reporte.objects.values_list('sucursal', flat=True).distinct(),
        'sucursal_seleccionada': sucursal,
        'buscar': buscar,  # сохраняем el término de búsqueda actual
    }
    return render(request, 'app/tabla_reportes.html', context)