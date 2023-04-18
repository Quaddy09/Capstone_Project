"""Capstone_Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
# from fingerpaint.views import Login, Homepage, Game, PasswordChange
from fingerpaint import views, routing, consumers

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Login.as_view()),
    path('password/', views.PasswordChange.as_view()),
    path('createuser/', views.CreateUser.as_view()),
    path('home/', views.Homepage.as_view()),
    path('home/<str:room_name>/', views.Game, name="game")
]

routing.websocket_urlpatterns = [
    path('ws://127.0.0.1:8000/ws/home/<str:room_name>', consumers.GameConsumer.as_asgi())
]

"""
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Login.as_view()),
    path('password/', views.PasswordChange.as_view()),
    path('createuser/', views.CreateUser.as_view()),
    path('home/', views.Homepage.as_view()),
    path('home/<str:room_name>/', views.Game, name="game"),
    path('video_feed/', views.video_feed, name='video_feed'),
]
"""