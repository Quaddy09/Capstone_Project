from django.shortcuts import render, redirect
from django.views import View
from .models import User
from classes import myUser


class Login(View):
    def get(self, request):
        return render(request, "Login.html", {})

    def post(self, request):
        attempted_username = request.POST['username']
        attempted_password = request.POST['password']

        message = ''
        print(request.POST)

        if 'signin' in request.POST:
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
        else:
            if myUser.create_user(attempted_username, attempted_password):
                message = 'Successfully created the user.'
            else:
                message = 'Failed to create user owing to double username.'
            return render(request, "Login.html", {"message": message})


class PasswordChange(View):
    def get(self, request):
        return render(request, "PasswordChange.html", {})

    def post(self, request):
        username = request.POST['username']
        new_pass = request.POST['password']
        myUser.set_password(username, new_pass)

        return render(request, "Login.html", {})


class Homepage(View):
    def get(self, request):
        my_user = myUser.get_user(request.session["session_username"])
        return render(request, "Home.html", {})

    #def post(self, request):
    #    my_user = myUser.get_user(request.session["session_username"])
    #    return render(request, "?????.html", {})


class Game(View):
    def get(self, request):
        return render(request, "Game.html", {})
