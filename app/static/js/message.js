// Connect to the WebSocket server
const socket = io('http://localhost:5000/messages');

// Function to join a room
function joinRoom(room) {
	socket.emit('join', { room: room });
}

// Function to leave a room
function leaveRoom(room) {
	socket.emit('leave', { room: room });
}

// Listening for incoming messages
socket.on('new_message', function (data) {
	if (data.receiver === currentUser.username) {
		displayNewMessage(data);
	}
});
