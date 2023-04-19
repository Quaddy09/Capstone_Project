//const room_name = document.currentScript.getAttribute('data-room-name');
//const room_name = JSON.parse(document.getElementById('room-name').textContent)
const room_name = document.getElementById("name")

// Create a new WebSocket instance
const socket = new WebSocket('ws://' + window.location.host + '/ws/home/' + room_name + '/');

socket.onmessage = function (e) {
  const data = JSON.parse(e.data);
  console.log(data);
}
/*
// Add an event listener for when the WebSocket connection is opened
socket.addEventListener('open', (event) => {
  // Send a message to the server
  socket.send('Hello Server!');
});

// Add an event listener for when a message is received from the server
socket.addEventListener('message', (event) => {
  // Parse the message as JSON
  const data = JSON.parse(event.data);

  // Retrieve the roomName value from the message
  const usernames = data.username;

  // Use the roomName value as needed
  console.log('roomName:', usernames);
});

// Add an event listener for when the WebSocket connection is closed
socket.addEventListener('close', (event) => {
  // Handle WebSocket close event
});
*/
