from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy


class CustomLoginView(LoginView):
  template_name = 'app/login.html'
  next_page = reverse_lazy('crear_reporte')
  def dispatch(self, request, *args, **kwargs):
    if self.request.user.is_authenticated:
      return redirect('crear_reporte')
    return super().dispatch(request, *args, **kwargs)