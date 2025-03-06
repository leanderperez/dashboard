// Script para mostrar el equipo segun la clasificacion
document.addEventListener('DOMContentLoaded', function() {
  const classificationSelect = document.getElementById('classification');
  const equipmentSelect = document.getElementById('equipment');

  const equipmentOptions = {
    'Infraestructura': ['Obra Civil', 'Electricidad', 'Herrería', 'Plomería', 'Carpintería', 'Cerrajería', 'Cristalería', 'Jardinería'],
    'Energía': ['Planta Eléctrica', 'Suministro Eléctrico'],
    'Refrigeración': ['Cava de Refrigerados', 'Cava de Congelados', 'Laboratorio', 'Compresor MT', 'Compresor BT', 'Rack de Compresores', 'Nevera Beluga', 'Nevera Valzer (Reachin)', 'Nevera Overture', 'Nevera de Barra', 'Thermo King', 'Bomba de Agua Helada', 'Nevera de Barra (Remota)', 'Nevera Mural (Remota)', 'Nevera Bahía (Remota)'],
    'Climatización': ['A/A Split', 'Chiller', 'Compresor', 'Unidad Condensadora', 'Cortina de Aire', 'Fancoil', 'UMA', 'Bomba de Agua Helada'],
    'Perecederos': ['Empaquetadora al Vacío', 'Molino', 'Ralladora', 'Rebanadora', 'Sierra'],
    'Lavandería': ['Lavadora', 'Secadora'],
    'Carga y Transporte': ['Ascensor','Carretilla', 'Cinta Transportadora', 'Elevador de Carga', 'Genie', 'Montacargas', 'Plataforma (Romana)', 'Portón', 'Santa María', 'Traspaleta', 'Trolley'],
    'Hidráulica': ['Bomba de Agua', 'Compresor de Aire', 'Filtro de Agua', 'Tanque Subterráneo', 'Tanque Aéreo', 'Calentador']
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

// Script para mostrar el encargado segun la categoría y el personal seleccionado
document.addEventListener('DOMContentLoaded', function() {
  const personalSelect = document.getElementById('personal');
  const classificationSelect = document.getElementById('classification');
  const encargadoSelect = document.getElementById('encargado');

  const encargadoOptions = {
    'Contratista': {
      'Energía': ['Top Generation', 'Plantas Modulares', 'Hema'],
      'Refrigeración': ['Tecnonorte', 'RSC', 'Tecniservicios JN'],
      'Climatización': ['Somago', 'Midea'],
      'Perecederos' : ['JCF', 'Rios Agua Viva', 'Tecnoembalaje'],
      'Lavandería' : ['Alberto Medina'],
      'Carga y Transporte' : ['KTM', 'Ascensores PP', 'Ascensores del Lago', 'Tecnivera', 'Yan Landaeta', 'Forkli'],
      'Hidráulica' : ['Hidrosoluciones', 'Jose Luís Peña'],
    },
    'Técnico de Cuadrilla': ['Tec. Oscar', 'Tec. Jean', 'Tec. Starlyn', 'Tec. Juan', 'Tec. Luis', 'Tec. Gustavo'],
    'Técnico de Infraestructura': ['Supervisor de Infraestructura']
  };

  function updateEncargadoOptions() {
    const selectedPersonal = personalSelect.value;
    const selectedClassification = classificationSelect.value;

    let options = [];

    if (selectedPersonal === 'Contratista') {
      options = (encargadoOptions[selectedPersonal] && encargadoOptions[selectedPersonal][selectedClassification]) || [];
    } else {
      options = encargadoOptions[selectedPersonal] || [];
    }

    encargadoSelect.innerHTML = '<option selected disabled value="">Encargado</option>';
    options.forEach(function(option) {
      const optionElement = document.createElement('option');
      optionElement.value = option;
      optionElement.textContent = option;
      encargadoSelect.appendChild(optionElement);
    });
  }

  personalSelect.addEventListener('change', function() {
    console.log('Personal select changed');
    updateEncargadoOptions();
  });

  classificationSelect.addEventListener('change', function() {
    console.log('Classification select changed');
    updateEncargadoOptions();
  });
});

// Valiador de formularios
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

//Script para carrousel de pendientes
var swiper = new Swiper('.blog-slider', {
  spaceBetween: 30,
  effect: 'fade',
  loop: true,
  mousewheel: {
    invert: false,
  },
  // autoHeight: true,
  pagination: {
    el: '.blog-slider__pagination',
    clickable: true,
  },
  autoplay: {
    delay: 4000,
    disableOnInteraction: false, // Permite que el autoplay continúe después de la interacción del usuario
  }
});