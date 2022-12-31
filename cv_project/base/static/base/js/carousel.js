const carousel = document.querySelector('.carousel');
let slides;
let currentSlide = 0;
let currentDirection = 'right';

function setCarousel() {
  // create <div class='slide'> with image and position
  for(let i = 0; i < 6; i++) {
    let slideDiv = document.createElement('div');
    slideDiv.classList.add('slide');
    slideDiv.style['left'] = `${i * 100}%`;
    slideDiv.style['background-image'] = `url(static/base/images/cv_template${i+1}.jpg)`;
    carousel.appendChild(slideDiv);
  }
  // init finished slides variable
  slides = carousel.querySelectorAll('.slide');
}

function goToSlide(index) {
  if (index < 0 || index >= slides.length) return;

  if (index > currentSlide) {
    slides.forEach((slide, id) => {
      slide.style.left = `${parseInt(slide.style.left) -100}%`;
    });
  } else {
    slides.forEach((slide, id) => {
      slide.style.left = `${parseInt(slide.style.left) + 100}%`;
    });
  }

  currentSlide = index;
}

const prevButton = document.querySelector('.prev-button');
const nextButton = document.querySelector('.next-button');

prevButton.addEventListener('click', () => {
  goToSlide(currentSlide - 1);
});

nextButton.addEventListener('click', () => {
  goToSlide(currentSlide + 1);
});

setCarousel();
setInterval(()=>{
  if(currentDirection === "right") {
    nextButton.click();
    if (currentSlide >= 6 - 1) currentDirection = 'left';
  } else {
    prevButton.click();
    if (currentSlide <= 0) currentDirection = 'right';
  }
}, 3000)
