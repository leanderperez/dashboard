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
        delay: 3000,
        disableOnInteraction: false, // Permite que el autoplay continúe después de la interacción del usuario
      }
    });