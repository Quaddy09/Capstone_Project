var room_name = document.getElementById("name").innerHTML;
room_name = room_name.trimStart();

// Create a new WebSocket instance
const socket = new WebSocket('ws://' + window.location.host + '/ws/home/' + room_name + '/');

socket.onmessage = function (e) {
  const data = JSON.parse(e.data);
  document.querySelector('#chat-log').value += (data.message + '\n');
}

socket.onclose = function(e) {
  console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
  if (e.keyCode === 13) {  // enter, return
    document.querySelector('#chat-message-submit').click();
  }
};

document.querySelector('#chat-message-submit').onclick = function(e) {
  const messageInputDom = document.querySelector('#chat-message-input');
  const message = messageInputDom.value;
  socket.send(JSON.stringify({
    'message': message
  }));
  messageInputDom.value = '';
};
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
