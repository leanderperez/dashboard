from django.urls import path
from app.views import reportes
from app.views import tabla

urlpatterns = [
    path('crear/', reportes.crear_reporte, name='crear_reporte'),
    path('modificar/<int:pk>/', reportes.modificar_reporte, name='modificar_reporte'),
    path('tabla/', tabla.tabla_reportes, name='tabla_reportes'),
]