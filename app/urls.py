from django.urls import path
from app.views import reportes, datatable, login, plot, pendientes, dashboard, requisiciones, materiales
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', login.CustomLoginView.as_view(), name='home'),
    path('accounts/login/', login.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('acceso-denegado/', login.acceso_denegado, name='acceso_denegado'),
    
    path('crear/', reportes.crear_reporte, name='crear_reporte'),
    path('modificar/<int:pk>/', reportes.modificar_reporte, name='modificar_reporte'),
    path('datatable/', datatable.datatable, name='datatable'),
    path('dashboard/', dashboard.index, name='dashboard'),
    path('plot/', plot.crear_plot, name='plot'),
    path('pendientes/', pendientes.pendientes, name='pendientes'),

    path('materiales/', materiales.lista_materiales, name='lista_materiales'),
    path('materiales/crear/', materiales.crear_material, name='crear_material'),
    path('materiales/editar/<int:pk>/', materiales.editar_material, name='editar_material'),
    path('materiales/eliminar/<int:pk>/', materiales.eliminar_material, name='eliminar_material'),
    
    path('solicitudes/', requisiciones.lista_solicitudes, name='lista_solicitudes'),
    path('solicitudes/<int:pk>/', requisiciones.detalle_solicitud, name='detalle_solicitud'),
    path('crear_solicitud_material/', requisiciones.crear_solicitud_material, name='crear_solicitud_material'),
    path('solicitudes/cambiar-estado/<int:pk>/<str:accion>/', requisiciones.cambiar_estado_solicitud, name='cambiar_estado_solicitud'),
    path('solicitudes/completar/<int:pk>/', requisiciones.completar_solicitud, name='completar_solicitud'),
    path('solicitudes/asignar-analista/<int:pk>/', requisiciones.asignar_analista, name='asignar_analista'),

    path('dashboard/grafico_clasificacion/', dashboard.grafico_clasificacion, name='grafico_clasificacion'),
    path('dashboard/grafico_sucursales/', dashboard.grafico_sucursales, name='grafico_sucursales'),
    path('dashboard/grafico_kilos/', dashboard.grafico_kilos, name='grafico_kilos'),
    path('dashboard/grafico_costos/', dashboard.grafico_costos, name='grafico_costos'),
]