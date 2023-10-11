var swiper = new Swiper(".mySwiper", {
    // autoplay: {
    //   //delay: 5000,
    //   delay: 12000,
    // },
    slidesPerView: 1,
    // spaceBetween: 30,
    grabCursor: true,
    loop: true,
    fade: "true",
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
    pagination: {
      el: ".swiper-pagination",
      clickable: true,
      dynamicBullets: true,
    },
    mousewheel: false,
    keyboard: false,
  });
  