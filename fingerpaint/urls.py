from django.urls import path
from fingerpaint import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.Login.as_view()),

    path('password/', views.PasswordChange.as_view()),
    path('createuser/', views.CreateUser.as_view()),

    path('home/', views.home, name="home"),
    path('home/<str:room_name>/', views.Game, name="game"),
    path('home/check_room/<str:room_name>/', views.roomExist, name="check_room"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
