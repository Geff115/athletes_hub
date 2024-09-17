/* JavaScript code for the slideshow */

// Ensuring DOM is fully loaded before running the script
document.addEventListener("DOMContentLoaded", function () {
	// Getting the slideshow element by its ID
	const slideshow = document.querySelector("#slideshow");

	// Initializing the carousel if its not automatically done by Bootstrap
	const carouselInstance = new bootstrap.Carousel(slideshow, {
		interval: 5000,
		wrap: true,
		pause: 'hover',
		ride: 'carousel'
	});

	// Listen to slide events
	slideshow.addEventListener('slid.bs.carousel', function (event) {
		console.log(`Slide ${event.to + 1} is now displayed`);
	});
});
