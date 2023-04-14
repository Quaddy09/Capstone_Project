from django.shortcuts import render, redirect
from django.views import View
from .models import User
from classes import myUser
from django.http.response import StreamingHttpResponse
from django.http import HttpResponse
import cv2


class Login(View):
    def get(self, request):
        return render(request, "Login.html")

    def post(self, request):
        attempted_username = request.POST['username']
        attempted_password = request.POST['password']

        if not myUser.exists(attempted_username):
            return render(request, "Login.html", {"message": "Incorrect username"})
        else:
            my_user = myUser.get_user(attempted_username)
            my_password = myUser.get_password(my_user)
        if not myUser.password_check(attempted_password, my_password):
            return render(request, "Login.html", {"message": "Incorrect password"})
        else:
            request.session["session_username"] = attempted_username
            request.session.set_expiry(0)
            return redirect("/home/")


class PasswordChange(View):
    def get(self, request):
        return render(request, "PasswordChange.html", {})

    def post(self, request):
        username = request.POST['username']
        new_pass = request.POST['password']
        if new_pass == "" or None:
            return render(request, 'PasswordChange.html', {'message': 'Password cannot be empty'})
        myUser.set_password(username, new_pass)
        return redirect("/")


class CreateUser(View):
    def get(self, request):
        return render(request, "CreateUser.html")

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        if myUser.exists(username):
            return render(request, "CreateUser.html", {"message": "That username already exists"})
        elif password == "" or None:
            return render(request, "CreateUser.html", {"message": "Password cannot be empty"})
        else:
            if myUser.create_user(username, password):
                return redirect("/")
            else:
                return render(request, "CreateUser.html", {"message": "Something went wrong"})


class Homepage(View):
    def get(self, request):
        my_user = myUser.get_user(request.session["session_username"])
        return render(request, "Home.html", {})


def Game(request, room_name):
    my_user = myUser.get_user(request.session["session_username"])
    return render(request, 'Game.html', {'data': my_user})


class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def video_feed(request):
    return StreamingHttpResponse(gen(VideoCamera()),
                    content_type='multipart/x-mixed-replace; boundary=frame')