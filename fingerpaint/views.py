import cv2

from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import Room
from classes import myUser
from django.http import JsonResponse



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


def home(request):
    return render(request, 'Home.html', {})


def Game(request, room_name):
    # my_user = myUser.get_user(request.session["session_username"])
    return render(request, 'Game.html', {
        'room_name': room_name
    })


@csrf_exempt
def roomExist(request, room_name):
    print(room_name)
    response = True
    try:
        Room.objects.get(room_name=room_name)
    except Room.DoesNotExist:
        response = False

    return JsonResponse({
        "room_exist": response
    })
