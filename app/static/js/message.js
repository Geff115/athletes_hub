// Connect to the WebSocket server
const socket = io('http://localhost:5000/messages');


// Handling the connection success event
socket.on('connection_success', (data) => {
	console.log(data.message);
});


// Function to join a room
function joinRoom(room) {
	socket.emit('join', { room: room });
}


// Function to leave a room
function leaveRoom(room) {
	socket.emit('leave', { room: room });
}


const form = document.getElementById('message-form');
const input = document.getElementById('message-input');

// Handle form submission
form.addEventListener('submit', function(event) {
	event.preventDefault();
	const messageContent = input.value;
	socket.emit('send_message', {
		'message': messageContent,
		'receiver_id': receiverId
	});
	input.value = '';
});



// Listening for incoming messages
socket.on('receive_message', function (data) => {
	const messageList = document.querySelector('#messages ul');
	const newMessage = document.createElement('li');
	newMessage.innerHTML = `<strong>${data.sender}:</strong> ${data.message} (${data.timestamp})`;
	messageList.appendChild(newMessage);
});

