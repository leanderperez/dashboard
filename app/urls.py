from django.urls import path
from app.views import reportes, datatable, login, plot, pendientes
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', login.CustomLoginView.as_view(), name='home'),
    path('accounts/login/', login.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('crear/', reportes.crear_reporte, name='crear_reporte'),
    path('modificar/<int:pk>/', reportes.modificar_reporte, name='modificar_reporte'),
    path('datatable/', datatable.datatable, name='datatable'),
    path('plot/', plot.crear_plot, name='plot'),
    path('pendientes/', pendientes.pendientes, name='pendientes')
]