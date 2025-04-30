from django.urls import path
from app.views import reportes, datatable, login, plot, pendientes, dashboard, requisiciones
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', login.CustomLoginView.as_view(), name='home'),
    path('accounts/login/', login.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('crear/', reportes.crear_reporte, name='crear_reporte'),
    path('modificar/<int:pk>/', reportes.modificar_reporte, name='modificar_reporte'),
    path('datatable/', datatable.datatable, name='datatable'),
    path('dashboard/', dashboard.index, name='dashboard'),
    path('plot/', plot.crear_plot, name='plot'),
    path('pendientes/', pendientes.pendientes, name='pendientes'),

    path('materiales/', requisiciones.lista_materiales, name='lista_materiales'),
    path('materiales/crear/', requisiciones.crear_material, name='crear_material'),
    path('materiales/editar/<int:pk>/', requisiciones.editar_material, name='editar_material'),
    path('materiales/eliminar/<int:pk>/', requisiciones.eliminar_material, name='eliminar_material'),
    path('solicitudes/', requisiciones.lista_solicitudes, name='lista_solicitudes'),
    path('solicitudes/<int:pk>/', requisiciones.detalle_solicitud, name='detalle_solicitud'),
    path('crear_solicitud_material/', requisiciones.crear_solicitud_material, name='crear_solicitud_material'),
    path('solicitudes/cambiar-estado/<uuid:token>/<str:accion>/', requisiciones.cambiar_estado_solicitud, name='cambiar_estado_solicitud')
]