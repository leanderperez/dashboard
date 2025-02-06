from django.urls import path
from app.views import reportes
from app.views import datatable

urlpatterns = [
    path('crear/', reportes.crear_reporte, name='crear_reporte'),
    path('modificar/<int:pk>/', reportes.modificar_reporte, name='modificar_reporte'),
    path('datatable/', datatable.datatable_reportes, name='datatable_reportes'),
]