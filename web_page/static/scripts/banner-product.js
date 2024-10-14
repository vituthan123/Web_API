let currentSlide = 0;
const slides = document.querySelectorAll('.slide');
const totalSlides = slides.length;

function nextSlide() {
  currentSlide = (currentSlide + 2) % totalSlides; // Chuyển đến 2 ảnh tiếp theo
  updateSlidePosition();
}

function backSlide() {
  if (currentSlide === 0) {
    currentSlide = totalSlides - 2; // Nếu đang ở slide 1, chuyển đến slide 4
  } else {
    currentSlide = (currentSlide - 2 + totalSlides) % totalSlides; // Chuyển đến 2 ảnh trước đó
  }
  updateSlidePosition();
}
function updateSlidePosition() {
  const slideWidth = slides[0].clientWidth;
  const bannerSlides = document.querySelector('.banner-slides');
  
    // Nếu không phải slide đầu tiên, sử dụng hiệu ứng chuyển đổi
  bannerSlides.style.transition = 'transform 1s ease-in-out';
  
  bannerSlides.style.transform = `translateX(${-currentSlide * (slideWidth+10)}px)`;

}

