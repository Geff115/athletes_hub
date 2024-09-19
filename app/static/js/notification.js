// Connecting to the WebSocket for notifications
const notificationSocket = io.connect('http://localhost:5000/notifications');

// Listening for new notifications
notificationSocket.on('new_notification', (data) => {
	console.log(`Notification: ${data.message}`);
	// Display the notification in the UI
	const notificationBox = document.querySelector('#notifications ul');
	const newNotification = document.createElement('li');
	newNotification.textContent = `Notification: ${data.message}`;
	notificationList.appendChild(newNotification);
});
