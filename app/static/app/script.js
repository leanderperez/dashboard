// Script para mostrar el equipo segun la clasificacion
document.addEventListener('DOMContentLoaded', function() {
  const classificationSelect = document.getElementById('classification');
  const equipmentSelect = document.getElementById('equipment');

  const equipmentOptions = {
    'Energía': ['Generador', 'Panel Solar'],
    'Refrigeración': ['Nevera', 'Congelador'],
    'Climatización': ['Aire Acondicionado', 'Ventilador'],
    'Laboratorio': ['Microscopio', 'Centrífuga'],
    'Lavandería': ['Lavadora', 'Secadora'],
    'Carga y Transporte': ['Camión', 'Montacargas']
  };

  classificationSelect.addEventListener('change', function() {
    const selectedClassification = classificationSelect.value;
    const options = equipmentOptions[selectedClassification] || [];

    equipmentSelect.innerHTML = '<option selected disabled value="">Equipo</option>';
    options.forEach(function(option) {
      const optionElement = document.createElement('option');
      optionElement.value = option;
      optionElement.textContent = option;
      equipmentSelect.appendChild(optionElement);
    });
  });
});

// Script para mostrar el encargado segun el personal seleccionado
document.addEventListener('DOMContentLoaded', function() {
  const personalSelect = document.getElementById('personal');
  const encargadoSelect = document.getElementById('encargado');

  const encargadoOptions = {
    'Contratista': ['Tecnonorte', 'Somago', 'JCF', 'KTM', 'Tecnoembalaje'],
    'Técnico de Cuadrilla': ['Tec. Oscar', 'Tec. Jean', 'Tec. Starlyn', 'Tec. Juan', 'Tec. Luis', 'Tec. Gustavo'],
    'Técnico de Infraestructura': ['Supervisor de Infraestructura']
  };

  personalSelect.addEventListener('change', function() {
    const selectedpersonal = personalSelect.value;
    const options = encargadoOptions[selectedpersonal] || [];

    encargadoSelect.innerHTML = '<option selected disabled value="">Encargado</option>';
    options.forEach(function(option) {
      const optionElement = document.createElement('option');
      optionElement.value = option;
      optionElement.textContent = option;
      encargadoSelect.appendChild(optionElement);
    });
  });
});

(function () {
  'use strict'
  const forms = document.querySelectorAll('.requires-validation')
  Array.from(forms)
    .forEach(function (form) {
      form.addEventListener('submit', function (event) {
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
        }
  
        form.classList.add('was-validated')
      }, false)
    })
  })()