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