let room_name = document.getElementById('room_name');

document.addEventListener("DOMContentLoaded", () => {
      var but = document.getElementById("try");
      var video = document.getElementById("vid");
      var mediaDevices = navigator.mediaDevices;
      vid.muted = true;
      but.addEventListener("click", () => {

        // Accessing the user camera and video.
        mediaDevices
          .getUserMedia({
            video: true,
            audio: true,
          })
          .then((stream) => {

            // Changing the source of video to current stream.
            video.srcObject = stream;
            video.addEventListener("loadedmetadata", () => {
              video.play();
            });
          })
          .catch(alert);
      });
});

function getInRoom() {
    if (!/^[a-zA-Z0-9-_]+$/.test(room_name.value)){
            alert("Error. Please use  underscore and alphanumeric only ! ");
        }
    else {
        window.location.href = window.location.href+ "" +room_name.value
    }
}

let create_room = document.getElementById("create_room");

create_room.addEventListener('click',async function(){
    try {
        const check_url = window.location.host
        const res = await fetch(`${check_url}/room/check_room/${room_name.value}/`,{
            method:'GET',
        })
        const r = await res.json()
        getInRoom()
    } catch (error) {
        console.log(error)
    }
})

function onClickVideo() {
    var modal = document.getElementById("videoModal");
    modal.style.display = "block";
}
function onClickVideoModal() {
    var modal = document.getElementById("videoModal");
    modal.style.display = "none";
}