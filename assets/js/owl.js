$('.owl-carousel').owlCarousel({
  loop: true,
  margin: 10,
  nav: true,
  navText: [
    "<img src='./static/img/VectorLeft.svg'>",
    "<img src='./static/img/VectorRight.svg' />"
  ],
  autoplay: false,
  autoplayHoverPause: false,
  responsive: {
    0: {
      items: 2
    },
    600: {
      items: 3
    },
    960: {
      items: 3
    },
    1300: {
      items: 5
    },
    1000: {
      items: 5
    }
  }
})