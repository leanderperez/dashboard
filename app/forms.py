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
    CLASIFICACIONES = (
        ('Energía', 'Energía'),
        ('Refrigeración', 'Refrigeración'),
        ('Climatización', 'Climatización'),
        ('Laboratorio', 'Laboratorio'),
        ('Lavandería', 'Lavandería'),
        ('Carga y Transporte', 'Carga y Transporte'),
    )
    FALLAS = (
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

    fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'id': 'fecha'}))
    sucursal = forms.ChoiceField(choices=SUCURSALES, label='Sucursal', widget=forms.Select(attrs={'class': 'form-control', 'id': 'sucursal'}))
    clasificacion = forms.ChoiceField(choices=CLASIFICACIONES, label='Clasificación', widget=forms.Select(attrs={'class': 'form-control', 'id': 'clasificacion'}))
    falla = forms.ChoiceField(choices=FALLAS, label='Falla o Motivo de Visita', widget=forms.Select(attrs={'class': 'form-control', 'id': 'falla'}))
    coordinador = forms.ChoiceField(choices=COORDINADORES, label='Coordinador', widget=forms.RadioSelect(attrs={'class': 'form-check-input', 'id': 'coordinador'}))

    def __init__(self, *args, **kwargs):
        super(ReporteForm, self).__init__(*args, **kwargs)
        self.fields['fecha'].widget.attrs.update({'class': 'form-control date-input'})
        self.fields['sucursal'].widget.attrs.update({'class': 'form-control select-input'})
        self.fields['clasificacion'].widget.attrs.update({'class': 'form-control select-input'})
        self.fields['falla'].widget.attrs.update({'class': 'form-control select-input'})
        self.fields['coordinador'].widget.attrs.update({'class': 'form-check-input btn-outline-secondary'})
        
        # Actualizar las clases de los labels
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})  # Actualiza la clase de los inputs
            field.label_tag = lambda label, attrs=None, label_suffix=None: f'<label class="form-label" for="{field.widget.attrs.get("id", field_name)}">{label}</label>'

class ReporteAdminForm(forms.ModelForm):
    class Meta:
        model = Reporte
        fields = '__all__'  # Todos los campos para el administrador