from django import forms
from ..models import Reporte, Material, SolicitudMaterial, DetalleSolicitud
from django.contrib.auth.forms import AuthenticationForm
from django.forms import inlineformset_factory

SUCURSALES = (
    ('', 'Sucursal'),
    ('Acarigua', 'Acarigua'),
    ('Altamira', 'Altamira'),
    ('Barquisimeto', 'Barquisimeto'),
    ('Cagua', 'Cagua'),
    ('CENDIS', 'CENDIS'),
    ('Charallave', 'Charallave'),
    ('Ciudad Bolívar', 'Ciudad Bolívar'),
    ('El Paraíso', 'El Paraíso'),
    ('Fuerte Tiuna', 'Fuerte Tiuna'),
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
    ('Infraestructura', 'Infraestructura'),
    ('Energía', 'Energía'),
    ('Refrigeración', 'Refrigeración'),
    ('Climatización', 'Climatización'),
    ('Perecederos', 'Perecederos'),
    ('Línea Blanca', 'Línea Blanca'),
    ('Carga y Transporte', 'Carga y Transporte'),
    ('Hidráulica', 'Hidráulica')
)
FALLAS = (
    ('', 'Falla o Motivo de Visita'),
    ('Falso Reporte', 'Falso Reporte'),
    ('Operación', 'Operación'),
    ('Mecánica', 'Mecánica'),
    ('Eléctrica', 'Eléctrica'),
    ('Control', 'Control'),
    ('Mantenimiento', 'Mantenimiento'),
    ('Preventivo', 'Preventivo'),
    ('Instalación', 'Instalación')
)
COORDINADORES = (
    ('', 'Coordiador'),
    ('Airam', 'Airam'),
    ('Carlos', 'Carlos'),
    ('Cesar', 'Cesar'),
    ('Edicson', 'Edicson'),
    ('Iriana', 'Iriana'),
    ('Juan', 'Juan'),
    ('Leander', 'Leander'),
)
EQUIPOS = (
    ('', 'Equipo'),

    ('Obra Civil', 'Obra Civil'),
    ('Electricidad', 'Electricidad'),
    ('Herrería', 'Herrería'),
    ('Plomería', 'Plomería'),
    ('Carpintería', 'Carpintería'),
    ('Cerrajería', 'Cerrajería'),
    ('Cristalería', 'Cristalería'),
    ('Jardinería', 'Jardinería'),

    ('Planta Eléctrica','Planta Eléctrica'),
    ('Suministro Eléctrico','Suministro Eléctrico'),

    ('Planta Eléctrica','Planta Eléctrica'),
    ('Suministro Eléctrico','Suministro Eléctrico'),
    ('Cava de Refrigerados','Cava de Refrigerados'),
    ('Cava de Congelados','Cava de Congelados'),
    ('Laboratorio','Laboratorio'),
    ('Compresor MT','Compresor MT'),
    ('Compresor BT','Compresor BT'),
    ('Rack de Compresores','Rack de Compresores'),
    ('Nevera Beluga','Nevera Beluga'),
    ('Nevera Valzer (Reachin)','Nevera Valzer (Reachin)'),
    ('Nevera Overture','Nevera Overture'),
    ('Nevera de Barra','Nevera de Barra'),
    ('Nevera de Barra (Remota)', 'Nevera de Barra (Remota)'),
    ('Nevera Mural (Remota)', 'Nevera Mural (Remota)'),
    ('Nevera Bahía (Remota)', 'Nevera Bahía (Remota)'),
    ('Thermo King','Thermo King'),
    ('Bomba de Agua Helada','Bomba de Agua Helada'),

    ('A/A Split','A/A Split'),
    ('Chiller','Chiller'),
    ('Compresor','Compresor'),
    ('Unidad Condensadora','Unidad Condensadora'),
    ('Cortina de Aire','Cortina de Aire'),
    ('Fancoil','Fancoil'),
    ('UMA','UMA'),
    ('Bomba de Agua Helada','Bomba de Agua Helada'),

    ('Empaquetadora al Vacío','Empaquetadora al Vacío'),
    ('Molino','Molino'),
    ('Ralladora','Ralladora'),
    ('Rebanadora','Rebanadora'),
    ('Sierra','Sierra'),

    ('Lavadora','Lavadora'),
    ('Secadora','Secadora'),
    ('Microondas','Microondas'),

    ('Ascensor','Ascensor'),
    ('Carretilla','Carretilla'),
    ('Cinta Transportadora','Cinta Transportadora'),
    ('Elevador de Carga','Elevador de Carga'),
    ('Genie','Genie'),
    ('Montacarga','Montacarga'),
    ('Plataforma (Romana)','Plataforma (Romana)'),
    ('Portón','Portón'),
    ('Santa María','Santa María'),
    ('Traspaleta','Traspaleta'),
    ('Trolley','Trolley'),

    ('Bomba de Agua','Bomba de Agua'),
    ('Compresor de Aire', 'Compresor de Aire'),
    ('Filtro de Agua','Filtro de Agua'),
    ('Tanque Subterráneo','Tanque Subterráneo'),
    ('Tanque Aéreo','Tanque Aéreo'),
    ('Calentador', 'Calentador')
)
PERSONAL = (
    ('', 'Personal'),
    ('Contratista', 'Contratista'),
    ('Técnico de Cuadrilla', 'Técnico de Cuadrilla'),
    ('Técnico de Infraestructura', 'Técnico de Infraestructura')
    )
ENCARGADOS = (
    ('', 'Encargado'),
    ('Top Generation', 'Top Generation'),
    ('Plantas Modulares', 'Plantas Modulares'),
    ('Hema', 'Hema'),
    ('Omega', 'Omega'),
    ('Tecnonorte', 'Tecnonorte'),
    ('RSC', 'RSC'),
    ('Tecniservicios JN', 'Tecniservicios JN'),
    ('Somago', 'Somago'),
    ('Midea', 'Midea'),
    ('JCF', 'JCF'),
    ('Rios Agua Viva', 'Rios Agua Viva'),
    ('Tecnoembalaje', 'Tecnoembalaje'),
    ('Alberto Medina', 'Alberto Medina'),
    ('KTM', 'KTM'),
    ('Ascensores PP', 'Ascensores PP'),
    ('Ascensores del Lago', 'Ascensores del Lago'),
    ('Tecnivera', 'Tecnivera'),
    ('Yan Landaeta', 'Yan Landaeta'),
    ('Forkli', 'Forkli'),
    ('Hidrosoluciones', 'Hidrosoluciones'),
    ('Jose Luís Peña', 'Jose Luís Peña'),
    ('Tec. Oscar', 'Tec. Oscar'),
    ('Tec. Jean', 'Tec. Jean'),
    ('Tec. Starlyn', 'Tec. Starlyn'),
    ('Tec. Juan', 'Tec. Juan'),
    ('Tec. Luis', 'Tec. Luis'),
    ('Tec. Gustavo', 'Tec. Gustavo'),
    ('Supervisor de Infraestructura', 'Supervisor de Infraestructura')
    )
REFRIGERANTES = (
    ('', 'Refrigerante'),
    ('R-22', 'R-22'),
    ('R-134a', 'R-134a'),
    ('R-290', 'R-290'),
    ('R-404A', 'R-404A'),
    ('R-410A', 'R-410A'),
    ('R-422', 'R-422'),
    ('R-600a', 'R-600a'),
    ('R-717 (NH3)', 'R-717 (NH3)'),
    ('R-718 (H2O)', 'R-718 (H2O)'),
    ('R-744 (CO2)', 'R-744 (CO2)'),
)
URGENCIAS = (
    ('Baja', 'Baja'),
    ('Media', 'Media'),
    ('Alta', 'Alta'),
)

class ReporteForm(forms.ModelForm):
    class Meta:
        model = Reporte
        fields = ['usuario', 'fecha', 'sucursal', 'clasificacion', 'equipo', 'reporte', 'falla', 'coordinador', 'observaciones', 'urgencia']  # Campos que puede rellenar el usuario

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
                                    widget=forms.Select(attrs={
                                        'class': 'form-select mt-3', 'id': 'coordinador'}))
    
    urgencia = forms.ChoiceField(choices=URGENCIAS, label='Urgencia', 
                                    widget=forms.RadioSelect(attrs={
                                        'class': 'btn-check'}))
    
    observaciones = forms.CharField(label='Observaciones',
                                    required=False,
                                    widget=forms.Textarea(attrs={
                                        'class': 'form-control mt-3',
                                        'id': 'observaciones',
                                        'placeholder': 'Ingrese su observación de forma concisa'}))

class ReporteAdminForm(forms.ModelForm):
    class Meta:
        model = Reporte
        fields = '__all__'  # Todos los campos para el administrador

    fecha = forms.DateField(label='Fecha',
                            widget=forms.DateInput(attrs={
                                'type': 'date', 
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
                                  'class': 'form-select mt-3',
                                   'id': 'falla'}))
    
    coordinador = forms.ChoiceField(choices=COORDINADORES, label='Coordinador', 
                                    widget=forms.Select(attrs={
                                        'class': 'form-select mt-3', 'id': 'coordinador'}))
    
    urgencia = forms.ChoiceField(choices=URGENCIAS, label='Urgencia', 
                                    widget=forms.RadioSelect(attrs={
                                        'class': 'btn-check'}))
    
    estatus = forms.BooleanField(label='Estatus',
                                 required=False, 
                                 widget=forms.CheckboxInput(attrs={
                                     'class': 'form-check-input', 
                                     'id': 'estatus'}))
    
    referencia = forms.CharField(label='Referencia',
                                required=False, 
                                widget=forms.TextInput(attrs={
                                'class': 'form-control', 
                                'id': 'referencia',
                                'placeholder': 'Referencia'}))
    
    personal = forms.ChoiceField(choices=PERSONAL, label='Personal',
                                 required=False, 
                                 widget=forms.Select(attrs={
                                     'class': 'form-select mt-3', 
                                     'id': 'personal'}))
    
    encargado = forms.ChoiceField(choices=ENCARGADOS, label='Encargado',
                                required=False, 
                                widget=forms.Select(attrs={
                                    'class': 'form-select mt-3', 
                                    'id': 'encargado'}))
    
    refrigerante = forms.ChoiceField(choices=REFRIGERANTES, label='Refrigerante',
                                    required=False, 
                                    widget=forms.Select(attrs={
                                        'class': 'form-select mt-3', 
                                        'id': 'refrigerante'}))
    
    kilos = forms.DecimalField(label='Kilos',
                                required=False, 
                                widget=forms.NumberInput(attrs={
                                    'class': 'form-control mt-3', 
                                    'id': 'kilos',
                                    'placeholder': 'Kilos'}))
    
    fecha_cierre = forms.DateField(label='Fecha de Cierre',
                                   required=False, 
                                   widget=forms.DateInput(attrs={
                                       'type': 'date',
                                       'class': 'form-control mt-3',
                                       'id': 'fecha_cierre',
                                       'placeholder': 'Fecha de Cierre'}))
    
    costo = forms.DecimalField(label='Costo',
                               required=False, 
                               widget=forms.NumberInput(attrs={
                                    'class': 'form-control mt-3', 
                                    'id': 'costo',
                                    'placeholder': 'Costo o Costo Estimado'}))
    
    gasto = forms.DecimalField(label='Costo',
                               required=False, 
                               widget=forms.NumberInput(attrs={
                                    'class': 'form-control mt-3', 
                                    'id': 'gasto',
                                    'placeholder': 'Gasto Realizado por Forum'}))
    
    ods_pdf = forms.FileField(label='ODS PDF',
                              required=False,
                              widget=forms.FileInput(attrs={
                                    'class': 'form-control mt-3', 
                                    'id': 'ods_pdf'}))
    
    observaciones = forms.CharField(label='Observaciones',
                                    required=False,
                                    widget=forms.Textarea(attrs={
                                        'class': 'form-control mt-3',
                                        'id': 'observaciones',
                                        'placeholder': 'Ingrese su observación de forma concisa'}))
    
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={'class': 'form-control mt-3',
                                      'placeholder': 'Usuario',
                                      'autocomplete' : 'off'}),
    )
    password = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control mt-3',
                                          'placeholder': 'Contraseña',
                                          'autocomplete' : 'off'}),
    )

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = '__all__'

    nombre = forms.CharField(label='Nombre',
                            widget=forms.TextInput(attrs={
                                'class': 'form-control mt-3', 
                                'id': 'nombre',
                                'placeholder': 'Nombre'}))
    
    descripcion = forms.CharField(label='Descripción',
                                   required=False, 
                                   widget=forms.Textarea(attrs={
                                       'class': 'form-control mt-3', 
                                       'id': 'descripcion',
                                       'placeholder': 'Descripción'}))
    
    unidad_medida = forms.CharField(label='Unidad de Medida',
                                    required=False, 
                                    widget=forms.TextInput(attrs={
                                        'class': 'form-control mt-3', 
                                        'id': 'unidad_medida',
                                        'placeholder': 'Unidad de Medida'}))

class SolicitudMaterialForm(forms.ModelForm):
    class Meta:
        model = SolicitudMaterial
        fields = ['sucursal', 'observaciones']

    sucursal = forms.ChoiceField(choices=SUCURSALES, label='Sucursal', 
                                 widget=forms.Select(attrs={
                                     'class': 'form-select mt-3', 
                                     'id': 'sucursal'}))
    
    observaciones = forms.CharField(label='Observaciones',
                                    required=False,
                                    widget=forms.Textarea(attrs={
                                        'class': 'form-control mt-3',
                                        'id': 'observaciones',
                                        'placeholder': 'Ingrese su observación de forma concisa'}))

DetalleSolicitudFormSet = inlineformset_factory(SolicitudMaterial, DetalleSolicitud, 
                                                fields=('material', 'cantidad'), 
                                                extra=1, 
                                                can_delete=False,
                                                widgets={
                                                    'material': forms.Select(attrs={'class': 'form-select mt-3'}),
                                                    'cantidad': forms.NumberInput(attrs={'value': 1, 'class': 'form-control'})})