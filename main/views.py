from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.utils.safestring import mark_safe

from django.forms import inlineformset_factory
from .forms import CreateUserForm

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

import json

# Create your views here.

def SignUp(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('login')
        # print(form)
        return render(request, 'authentication/signup.html', {'form':form})

def Login(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password =request.POST.get('password')
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.info(request, 'Username OR password is incorrect')
        
        context = {}
        return render(request, 'authentication/login.html', context)

def Logout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def index(request):
    return render(request , 'main/index.html')

@login_required(login_url='login')
def room(request , room_name):
    return render(request , 'main/room.html' , {
        'room_name' : mark_safe(json.dumps(room_name)),
        'logged_in_user' : request.user.username.capitalize(),
        'username' : mark_safe(json.dumps(request.user.username)),
    })