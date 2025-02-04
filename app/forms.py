from django import forms
from .models import Reporte

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
PERSONAL = (
    ('', 'Personal'),
    ('Contratista', 'Contratista'),
    ('Técnico de Cuadrilla', 'Técnico de Cuadrilla'),
    ('Técnico de Infraestructura', 'Técnico de Infraestructura')
    )
ENCARGADOS = (
    ('', 'Encargado'),
    ('Tecnonorte', 'Tecnonorte'),
    ('Somago', 'Somago'),
    ('JCF', 'JCF'),
    ('KTM', 'KTM'),
    ('Tecnoembalaje', 'Tecnoembalaje'),
    ('Tec. Oscar', 'Tec. Oscar'),
    ('Tec. Jean', 'Tec. Jean'),
    ('Tec. Starlyn', 'Tec. Starlyn'),
    ('Tec. Juan', 'Tec. Juan'),
    ('Tec. Luis', 'Tec. Luis'),
    ('Tec. Gustavo', 'Tec. Gustavo'),
    ('Supervisor de Infraestructura', 'Supervisor de Infraestructura')
    )

class ReporteForm(forms.ModelForm):
    class Meta:
        model = Reporte
        fields = ['fecha', 'sucursal', 'clasificacion', 'equipo', 'reporte', 'falla', 'coordinador', 'estatus']  # Campos que puede rellenar el usuario

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
                                  'id': 'reporte',
                                  'placeholder': 'Reporte'}))
    
    falla = forms.ChoiceField(choices=FALLAS, label='Falla o Motivo de Visita', 
                              widget=forms.Select(attrs={
                                  'class': 'form-select mt-3', 'id': 'falla'}))
    
    coordinador = forms.ChoiceField(choices=COORDINADORES, label='Coordinador', 
                                    widget=forms.RadioSelect(attrs={
                                        'class': 'btn-check', 'autocomplete': 'off'}), 
                                    required=True)
    
    estatus = forms.BooleanField(label='Estatus',
                                 required=False, 
                                 widget=forms.CheckboxInput(attrs={
                                     'class': 'form-check-input', 
                                     'id': 'estatus'}))

class ReporteAdminForm(forms.ModelForm):
    class Meta:
        model = Reporte
        fields = '__all__'  # Todos los campos para el administrador
        #fields = ['fecha', 'sucursal', 'clasificacion', 'equipo', 'reporte', 'falla', 'coordinador', 'estatus']

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
                                  'id': 'reporte',
                                  'placeholder': 'Reporte'}))
    
    falla = forms.ChoiceField(choices=FALLAS, label='Falla o Motivo de Visita', 
                              widget=forms.Select(attrs={
                                  'class': 'form-select mt-3', 'id': 'falla'}))
    
    coordinador = forms.ChoiceField(choices=COORDINADORES, label='Coordinador', 
                                    widget=forms.RadioSelect(attrs={
                                        'class': 'btn-check', 'autocomplete': 'off'}), 
                                    required=True)
    
    estatus = forms.BooleanField(label='Estatus',
                                 required=False, 
                                 widget=forms.CheckboxInput(attrs={
                                     'class': 'form-check-input', 
                                     'id': 'estatus'}))
    
    referencia = forms.CharField(label='Referencia', 
                                 widget=forms.TextInput(attrs={
                                  'class': 'form-control', 
                                  'id': 'referencia',
                                  'placeholder': 'Referencia'}))
    
    personal = forms.ChoiceField(choices=PERSONAL, label='Personal',
                                 widget=forms.Select(attrs={
                                     'class': 'form-select mt-3', 
                                     'id': 'personal'}))
    
    encargado = forms.ChoiceField(choices=ENCARGADOS, label='Encargado',
                                    widget=forms.Select(attrs={
                                        'class': 'form-select mt-3', 
                                        'id': 'encargado'}))
    
    fecha_cierre = forms.DateField(label='Fecha de Cierre',
        widget=forms.DateInput(attrs={'type': 'date', 
                                      'class': 'form-select mt-3', 
                                      'id': 'fecha_cierre'}))
    
    costo = forms.DecimalField(label='Costo',
                                widget=forms.NumberInput(attrs={
                                    'class': 'form-select mt-3', 
                                    'id': 'costo',
                                    'placeholder': 'Costo'}))
    
    ods_pdf = forms.FileField(label='ODS PDF',
                                widget=forms.FileInput(attrs={
                                    'class': 'form-select mt-3', 
                                    'id': 'ods_pdf'}))