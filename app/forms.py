from django import forms
from .models import Reporte

class ReporteForm(forms.ModelForm):
    class Meta:
        model = Reporte
        fields = ['fecha', 'sucursal', 'clasificacion', 'equipo', 'reporte', 'falla', 'coordinador', 'estatus']  # Campos que puede rellenar el usuario

    SUCURSALES = (
        ('Acarigua', 'Acarigua'),
        ('Barquisimeto', 'Barquisimeto'),
        ('Cagua', 'Cagua'),
        ('Charallave', 'Charallave'),
        ('Ciudad Bolívar', 'Ciudad Bolívar'),
        ('El Paraíso', 'El Paraíso'),
        ('Guarenas', 'Guarenas'),
        ('Guatire', 'Guatire'),
        ('Humbolt', 'Humbolt'),
        ('IPSFA', 'IPSFA'),
        ('La California', 'La California'),
        ('La Cascada', 'La Cascada'),
        ('La Hoyada', 'La Hoyada'),
        ('La Isabelica', 'La Isabelica'),
        ('La Piramide', 'La Piramide'),
        ('La Urbina', 'La Urbina'),
        ('Mañongo', 'Mañongo'),
        ('Maracay', 'Maracay'),
        ('Maturín Centro', 'Maturín Centro'),
        ('Monagas Plaza', 'Monagas Plaza'),
        ('Plaza Venezuela', 'Plaza Venezuela'),
        ('San Bernardino', 'San Bernardino'),
        ('San Martín', 'San Martín'),
        ('Santa Cecília', 'Santa Cecília')
    )
    sucursal = forms.ChoiceField(choices=SUCURSALES, label='Estado')

    CLASIFICACIONES = (
        ('Energía', 'Energía'),
        ('Refrigeración', 'Refrigeración'),
        ('Climatización', 'Climatización'),
        ('Laboratorio', 'Laboratorio'),
        ('Lavandería', 'Lavandería'),
        ('Carga y Transporte', 'Carga y Transporte'),
    )
    clasificacion = forms.ChoiceField(choices=CLASIFICACIONES, label='Clasificación')

class ReporteAdminForm(forms.ModelForm):
    class Meta:
        model = Reporte
        fields = '__all__'  # Todos los campos para el administrador