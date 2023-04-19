from django.urls import path
from fingerpaint import views


urlpatterns = [
    path('', views.Login.as_view()),

    path('password/', views.PasswordChange.as_view()),
    path('createuser/', views.CreateUser.as_view()),
    path('video_feed/', views.video_feed, name='video_feed'),

    path('home/', views.Homepage.as_view()),
    path('home/<str:room_name>/', views.Game, name="game"),
]
