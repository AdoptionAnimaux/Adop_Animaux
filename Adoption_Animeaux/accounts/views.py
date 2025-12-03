from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login, logout

from .forms import RegisterForm
from .models import UserProfile

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )

            UserProfile.objects.create(
                user=user,
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
                phone=form.cleaned_data["phone"],
            )

            login(request, user)
            return redirect("home")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})

from services.consul_client import get_service_url

def login_view(request):
    if request.method == "POST":
        user = authenticate(...)
        if user:
            login(request, user)

            url = get_service_url("adoption-service") + "/animals/"
            return redirect(url)

    return render(request, "login.html")

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('login')
    # GET -> show confirmation page
    return render(request, 'accounts/logout_confirm.html')