from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from app.forms import forms


class CustomLoginView(LoginView):
  template_name = 'app/login.html'
  next_page = reverse_lazy('crear_reporte')
  form_class = forms.CustomAuthenticationForm

  def dispatch(self, request, *args, **kwargs):
    if self.request.user.is_authenticated:
      return redirect('crear_reporte')
    return super().dispatch(request, *args, **kwargs)
  
# Función para verificar si el usuario está en el grupo "Coordinadores"
def is_coordinador(user):
    return user.groups.filter(name='Coordinadores').exists()

def acceso_denegado(request):
    return render(request, 'app/acceso_denegado.html')