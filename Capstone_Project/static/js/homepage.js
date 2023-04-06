let room_name = document.getElementById('room_name');
let create_room_btn = document.getElementById("create_room");
let join_room_btn = document.getElementById("join_room")

/* Checks that Room text box value is valid
*  If it is -> Redirects user to that "room" within game page */
function getInRoom() {
    if (!/^[a-zA-Z0-9-_]+$/.test(room_name.value)){
            alert("Error. Please use  underscore and alphanumeric only ! ");
        }
    else {
        window.location.href = window.location.href+ "" +room_name.value
    }
}

/* Adds click listener to create_room button
*  Checks to make sure room name isn't already used
*  calls function getInRoom() */
create_room_btn.addEventListener('click',async function(){
    try {
        const check_url = window.location.host
        const res = await fetch(`${check_url}/room/check_room/${room_name.value}/`,{
            method:'GET',
        })
        const r = await res.json()
        //if(r.room_exist){
        //    Swal.fire("Room Name Taken", "Please choose other or join this room ! ", "error");
        //}
        //else{
        getInRoom()
        //}
    } catch (error) {
        console.log(error)
    }
})
/* Adds click listener to join_room button*/
join_room_btn.addEventListener('click',getInRoom)

/*
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

function onClickVideo() {
    var modal = document.getElementById("videoModal");
    modal.style.display = "block";
}
function onClickVideoModal() {
    var modal = document.getElementById("videoModal");
    modal.style.display = "none";
}
*/