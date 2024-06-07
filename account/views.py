from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ChangeUserPasswordForm


def loginView(request):
    if request.user.is_authenticated:
        return redirect("home:index")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home:index")
        else:
            return render(request, "account/login.html", {
                "error": "Check your username or password!"
            })

    return render(request, "account/login.html")


def register(request):
    if request.user.is_authenticated:
        return redirect("home:index")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        repassword = request.POST["repassword"]

        if password == repassword:
            if User.objects.filter(username=username).exists():
                return render(request, "account/register.html",
                              {
                                  "error": "Username is already used!",
                                  "username": username,
                              })
            
            else:
                user = User.objects.create_user(username=username, email=email, first_name=firstname, password=password)
                user.save()
                login(request, user)

                return redirect("home:index")       
        else:
            return render(request, "account/register.html", {
                "error": "Passwords does not match!",
                "username": username,
            })

    return render(request, "account/register.html")


@login_required
def logoutView(request):
    logout(request)
    return redirect("account:login")
