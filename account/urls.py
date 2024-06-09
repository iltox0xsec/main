from django.urls import path
from .views import *

app_name = "account"
urlpatterns = [
    path("login/", loginView, name="login"),
    path("register/", register, name="register"),
    path("logout/", logoutView, name="logout"),
    path("profile/", profile, name="profile"),
    path("change/password/", changeUserPassword, name="changeUserPassword"),
]