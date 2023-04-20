let room_name = document.getElementById("name").innerHTML;
room_name = room_name.trimStart();
let player_list;
let draw_word_list = [
    'flower', 'balloons', 'the sun', 'trees', 'snake', 'dog', 'cat', 'car', 'fish', 'bird'
];
let correct_word;

// Create a new WebSocket instance
const socket = new WebSocket('ws://' + window.location.host + '/ws/home/' + room_name + '/');

socket.onopen = function(e) {
  console.log('socket connection established');
  /* join user to room */
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
      player_list = data['players'];
      updatePlayerList(data['players']);
      break;
    case 'start_game':
      let s_button = document.getElementById('start-game');
      s_button.disabled = true;

      const chosenPlayer = data['chosen_player'];
      let current_user = data['current_user'];
      if (chosenPlayer === current_user) {
        let randomIndex = Math.floor(Math.random() * draw_word_list.length);
        correct_word = draw_word_list[randomIndex];
        document.getElementById('guess-word').innerHTML = correct_word;
      }
      else {
        let s_button = document.getElementById('start-webcam');
        s_button.disabled = true;
        let stop_b = document.getElementById('stop-webcam');
        stop_b.disabled = true;
      }
      break;
    // get message data
    case 'message':
      let message = data['message'];
      let user = data['user'];
      if (message !== null && message !== '') {
        document.querySelector('#chat-log').value += (user + ': ' + message + '\n');
        if (message === correct_word) {
          console.log('you did it');
          document.querySelector('#chat-log').value += (user + ' guessed the right word!' + '\n');
          document.querySelector('#chat-log').value += ('moving to next person' + '\n');
          let stop_cam = document.getElementById('stop-webcam');
          stop_cam.click();
          socket.send(JSON.stringify({
            'command': 'start_game',
          }));
        }
      }
      break;
    default:
      console.log('unknown command');
      break;
  }
};

/* chat socket closes */
socket.onclose = function(e) {
  console.error('Connection Closed');
};

document.querySelector('#start-game').onclick = function(e) {
  socket.send(JSON.stringify({
    'command': 'start_game',
  }));
}

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
