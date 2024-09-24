// Function to toggle dark mode
function toggleDarkMode() {
	const body = document.body;
	const currentMode = localStorage.getItem('theme');

	// If currently dark mode, switch to light mode, otherwise switch to dark mode
	if (currentMode === 'dark') {
		body.classList.remove('dark-mode');
		body.classList.add('light-mode');
		localStorage.setItem('theme', 'light');
	} else {
		body.classList.remove('light-mode');
		body.classList.add('dark-mode');
		localStorage.setItem('theme', 'dark');
	}
}

// Modifying the button text to dynamically show "Light Mode" when dark mode is enabled
function updateToggleButton() {
	const currentMode = localStorage.getItem('theme');
	const toggleButton = document.getElementById('toggle-dark-mode');

	if (currentMode === 'dark') {
		toggleButton.innerHTML = '<i class="bi bi-brightness-high me-2"></i>Light Mode';
	} else {
		toggleButton.innerHTML = '<i class="bi bi-moon me-2"></i>Dark Mode';
	}
}

document.addEventListener('DOMContentLoaded', function () {
	const savedTheme = localStorage.getItem('theme') || 'light';
	document.body.classList.add(savedTheme + '-mode');
	updateToggleButton(); // Update the button text after the mode changes
	
	// Toggle dark mode on button click
	document.getElementById('toggle-dark-mode').addEventListener('click', function (e) {
		e.preventDefault();
		toggleDarkMode();
		updateToggleButton(); // Update the button text after the mode changes
	});
});
