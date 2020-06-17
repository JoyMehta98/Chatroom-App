from django.urls import path
from . import views


urlpatterns = [
    path('' , views.index , name="index"),
    path('login' , views.Login , name="login"),
    path('signup' , views.SignUp , name="signup"),
    path('logout' , views.Logout , name="logout"),
    path('<str:room_name>/' , views.room , name="room"),
]