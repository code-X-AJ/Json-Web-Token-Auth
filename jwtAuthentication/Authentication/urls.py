from django.contrib import admin
from django.urls import include, path
from Authentication.views import *


# it handles the urls dispatching
urlpatterns = [

    # for register/signup the user
    path('register', Register.as_view()),

    # to login the user
    path('login', Login.as_view()),

    # to see the dashboard as user logged in
    path('user', UserView.as_view()),

    # to logout the user, after this user wont be able to enter without loging in again 
    path('logout', Logout.as_view()),

    # to handel the image request and image manipulation
    path('profile', Profiles.as_view()),


]
