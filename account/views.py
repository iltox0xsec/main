from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ChangeUserPasswordForm
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import PasswordChangeForm





from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

def loginView(request):
    if request.user.is_authenticated:
        return redirect("home:index")

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home:index')
            else:
                return render(request, 'account/login.html', {'form': form})
    else:
        form = AuthenticationForm()
    return render(request, 'account/login.html', {'form': form})

def lockout(request, credentials, *args, **kwargs):
    return render(request, 'axes/locked_out.html')

def register(request):
    if request.user.is_authenticated:
        return redirect("home:index")

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('account:login')
    else:
        form = CustomUserCreationForm()
        print(form)
    return render(request, 'account/register.html', {'form': form})

@login_required
def logoutView(request):
    logout(request)
    return redirect("home:index")

@login_required
def profile(request):
    return render(request, 'account/profile.html')

@login_required 
def changeUserPassword(request):

    form = ChangeUserPasswordForm(data=request.POST, user=request.user)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            user = authenticate(request, username=request.user.username, password=form.new_password2)
            login(request, user)
            messages.success(
                request, 'Your password has been successfully updated.')
            return redirect("account:profile")

    context = {
        'form': form
    }
    return render(request, 'account/change_password.html', context)