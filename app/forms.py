from django import forms
from .models import Reporte

class ReporteForm(forms.ModelForm):
    class Meta:
        model = Reporte
        fields = ['fecha', 'sucursal', 'clasificacion', 'equipo', 'reporte', 'falla', 'coordinador']  # Campos que puede rellenar el usuario
    
    SUCURSALES = (
        ('', 'Sucursal'),
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
    CLASIFICACIONES = (
        ('', 'Clasificación'),
        ('Energía', 'Energía'),
        ('Refrigeración', 'Refrigeración'),
        ('Climatización', 'Climatización'),
        ('Laboratorio', 'Laboratorio'),
        ('Lavandería', 'Lavandería'),
        ('Carga y Transporte', 'Carga y Transporte'),
    )
    FALLAS = (
        ('', 'Falla o Motivo de Visita'),
        ('Falso Reporte', 'Falso Reporte'),
        ('Operación', 'Operación'),
        ('Mecánica', 'Mecánica'),
        ('Eléctrica', 'Eléctrica'),
        ('Control', 'Control'),
        ('Mantenimiento', 'Mantenimiento'),
        ('Preventivo', 'Preventivo')
    )
    COORDINADORES = (
        ('Cesar', 'Cesar'),
        ('Edicson', 'Edicson'),
        ('Iriana', 'Iriana'),
        ('Leander', 'Leander'),
    )
    EQUIPOS = (
        ('', 'Equipo'),
        ('Generador', 'Generador'),
        ('Panel Solar', 'Panel Solar'),
        ('Nevera', 'Nevera'),
        ('Congelador', 'Congelador'),
        ('Aire Acondicionado', 'Aire Acondicionado'),
        ('Ventilador', 'Ventilador'),
        ('Microscopio', 'Microscopio'),
        ('Centrífuga', 'Centrífuga'),
        ('Lavadora', 'Lavadora'),
        ('Secadora', 'Secadora'),
        ('Camión', 'Camión'),
        ('Montacargas', 'Montacargas')
    )

    fecha = forms.DateField(label='Sucursal',
        widget=forms.DateInput(attrs={'type': 'date', 
                                      'class': 'form-control', 
                                      'id': 'fecha'}))
    
    sucursal = forms.ChoiceField(choices=SUCURSALES, label='Sucursal', 
                                 widget=forms.Select(attrs={
                                     'class': 'form-select mt-3', 
                                     'id': 'sucursal'}))
    
    clasificacion = forms.ChoiceField(choices=CLASIFICACIONES, label='Clasificación', 
                                      widget=forms.Select(attrs={
                                          'class': 'form-select mt-3', 
                                          'id': 'classification'}))
    
    equipo = forms.ChoiceField(choices=EQUIPOS, label='Equipo', 
                             widget=forms.Select(attrs={
                                 'class': 'form-select mt-3', 
                                 'id': 'equipment'}))
    
    reporte = forms.CharField(label='Reporte', 
                              widget=forms.TextInput(attrs={
                                  'class': 'form-control', 
                                  'id': 'reporte'}))
    
    falla = forms.ChoiceField(choices=FALLAS, label='Falla o Motivo de Visita', 
                              widget=forms.Select(attrs={
                                  'class': 'form-select mt-3', 'id': 'falla'}))
    
    coordinador = forms.ChoiceField(choices=COORDINADORES, label='Coordinador', 
                                    widget=forms.RadioSelect(attrs={
                                        'class': 'btn-check', 'autocomplete': 'off'}), 
                                    required=True)


class ReporteAdminForm(forms.ModelForm):
    class Meta:
        model = Reporte
        fields = '__all__'  # Todos los campos para el administrador