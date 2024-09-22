/* Handling the role selection of a User in the signup page */

document.addEventListener('DOMContentLoaded', function () {
	const roleField = document.getElementById('role');
	const athleteFields = document.getElementById('athlete-fields');
	const scoutFields = document.getElementById('scout-fields');

	roleField.addEventListener("change", function() {
		const isAthlete = this.value === "Athlete";
		const isScout = this.value === "Scout";

		// Show/Hide based on the selected role
		athleteFields.style.display = isAthlete ? "block" : "none";
		scoutFields.style.display = isScout ? "block" : "none";

		// Handle required attributes
		document.getElementById("inputPosition").required = isAthlete;
		document.getElementById("inputSkills").required = isAthlete;
		document.getElementById("inputAchievements").required = isAthlete;

		document.getElementById("inputExperienceYears").required = isScout;
		document.getElementById("inputCredentials").required = isScout;
	});
});
