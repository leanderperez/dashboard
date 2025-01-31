from django.urls import path
from . import views

urlpatterns = [
    path('crear/', views.crear_reporte, name='crear_reporte'),
    path('modificar/<int:pk>/', views.modificar_reporte, name='modificar_reporte')
]