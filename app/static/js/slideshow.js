/* JavaScript code for the slideshow */

const heroElement = document.querySelector('.hero');
const images = ['/img/BAL1.jpg', '/img/BAL2.jpg', '/img/BAL3.jpg'];
let currentIndex = 0;

function showImage(index) {
	heroElement.style.backgroundImage = `url(${images[index]})`;
}

setInterval(() => {
	currentIndex = (currentIndex + 1) % images.length;
	showImage(currentIndex);
}, 3000); // slide speed
