var room_name = document.getElementById("name").innerHTML;
room_name = room_name.trimStart();

// Create a new WebSocket instance
const socket = new WebSocket('ws://' + window.location.host + '/ws/home/' + room_name + '/');

socket.onopen = function(e) {
  console.log('socket connection established');

  /* handle user list on socket connection */
  socket.send(JSON.stringify({
    'command': 'get_players'
  }))
}

/* update chat log with new message for all user */
socket.onmessage = function (e) {
  const data = JSON.parse(e.data);

  switch (data['command']) {
    // get list of players
    case 'players_list':
      const players = data['players'];
      console.log('list of players: ', players);
      break;
    // get message data
    case 'new_message':
      const message = data['message'];
      document.querySelector('#chat-log').value += (message + '\n');
      break;
    default:
      console.log('unknown command');
      break;
  }

  //document.querySelector('#chat-log').value += (data.message + '\n');
};

/* the chat socket closes */
socket.onclose = function(e) {
  console.error('Chat socket closed unexpectedly');
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
