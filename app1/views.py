from django.shortcuts import render, redirect
from .models import CustomUser
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
import re

# Create your views here.
@login_required(login_url='login')
def Home(request):
    return render(request,"home.html")

def Register(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        phone_number = request.POST["phone_number"]
        date_of_birth = request.POST["date_of_birth"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if not re.match(r'^\d{10}$', phone_number):
            messages.error(request, "Phone number must be exactly 10 digits.")
            return render(request, "register.html")
        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists.")
            return render(request, "register.html")

        if password1 != password2:
            messages.error(request, "passwords donot match")
            return render(request, "register.html")
        try:
            my_user = CustomUser.objects.create_user(
                username=email,
                email=email,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                date_of_birth=date_of_birth,
                password=password1)
            my_user.save()
            messages.success(request,"Your account has been created")
            return redirect('home')
        
        except ValidationError as e:
            messages.error(request, f"Error: {e}")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {e}")
    return render (request, "register.html")

def Login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        user = authenticate(request, username = email, password = password)
        if user is not None :
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")
    return render (request, "login.html")

def Logout(request):
    logout(request)
    return redirect('login')