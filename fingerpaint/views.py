from django.shortcuts import render, redirect
from django.views import View
#from .models import *
from classes import myUser


class Login(View):
    def get(self, request):
        return render(request, "Login.html", {})

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


class Homepage(View):
    def get(self, request):
        my_user = myUser.get_user(request.session["session_username"])
        return render(request, "Home.html", {})

    #def post(self, request):
    #    my_user = myUser.get_user(request.session["session_username"])
    #    return render(request, "?????.html", {})


class Lobby(View):
    def get(self, request):
        return render(request, "Lobby.html", {})


class Game(View):
    def get(self, request):
        return render(request, "Game.html", {})
