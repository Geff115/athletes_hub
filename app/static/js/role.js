/* Handling the role selection of a User in the signup page */

document.addEventListener('DOMContentLoaded', function () {
	const roleField = document.getElementById('role');
	const athleteFields = document.getElementById('athlete-fields');
	const scoutFields = document.getElementById('scout-fields');

	function toggleRequired(state, fields) {
		fields.forEach(field => {
			const input = document.getElementById(field);
			if (input) {
				input.required = state;
				input.disabled = !state;
			}
		});
	}

	function updateFields() {
		const isAthlete = roleField.value === "Athlete";
		const isScout = roleField.value === "Scout";

		// Show/Hide based on the selected role
		athleteFields.style.display = isAthlete ? "block" : "none";
		scoutFields.style.display = isScout ? "block" : "none";

		// Handle required attributes for athletes fields
		toggleRequired(isAthlete, ['inputPosition', 'inputSkills', 'inputAchievements']);

		// Handling required attributes for scouts fields
		toggleRequired(isScout, ['inputExperienceYears', 'inputCredentials']);
	}

	// Trigger on page load to set initial state
	updateFields();

	// Trigger on role change
	roleField.addEventListener("change", updateFields);
});
