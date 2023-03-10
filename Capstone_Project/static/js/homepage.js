let but = document.getElementById("try");
let video = document.getElementById("vid");
let mediaDevices = navigator.mediaDevices;

but.addEventListener("click", () => {

    mediaDevices.getUserMedia({
        video: true,
        audio: true,
    })
        .then((stream) => {
            video.srcObject = stream;
            video.addEventListener("loadmetadata", () => {
                video.play();
            });
        })
        .catch(alert);
});