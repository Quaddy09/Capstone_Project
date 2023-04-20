var room_name = document.getElementById("name").innerHTML;
room_name = room_name.trimStart();

// Create a new WebSocket instance
const socket = new WebSocket('ws://' + window.location.host + '/ws/home/' + room_name + '/');

socket.onopen = function(e) {
  console.log('socket connection established');
  /* handle user list on socket connection */
  socket.send(JSON.stringify({
    'command': 'join'
  }));
}

/* update chat log with new message for all user */
socket.onmessage = function (e) {
  const data = JSON.parse(e.data);
  console.log(data['command']);

  switch (data['command']) {
    // get list of players
    case 'join':
      console.log(data['players']);
      updatePlayerList(data['players']);
      break;
    case 'remove_player':
      break;
    // get message data
    case 'message':
      const message = data['message'];
      document.querySelector('#chat-log').value += (message + '\n');
      break;
    default:
      console.log('unknown command');
      break;
  }
};

/* the chat socket closes */
socket.onclose = function(e) {
  console.error('Connection Closed');
};



/* keyboard enter = send chat button */
document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
  if (e.keyCode === 13) {  // enter, return
    document.querySelector('#chat-message-submit').click();
  }
};

/* send user chat message through socket to everyone */
document.querySelector('#chat-message-submit').onclick = function(e) {
  const messageInputDom = document.querySelector('#chat-message-input');
  const message = messageInputDom.value;
  socket.send(JSON.stringify({
    'command': 'new_message',
    'message': message
  }));
  messageInputDom.value = '';
};

function updatePlayerList(array) {
  const playerListElement = document.getElementById('player-list');
  playerListElement.innerHTML = '';
  for (let i = 0; i < array.length; i++) {
    const listItem = document.createElement('li');
    const username = document.createTextNode(array[i]);
    listItem.appendChild(username);
    playerListElement.appendChild(listItem);
  }
}
