from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import UserForm
from django.contrib import messages 

# Create your views here.


def select_signup(request):
    return render(request, 'select_signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            err_msg = "아이디 혹은 비밀번호를 확인해주세요"
            return render(request, 'login.html', {'err_msg': err_msg})
    else:
        return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('/')

def signup_view(request, user_type):
    if request.method == "POST":
        # method가 post 일 때
        form = UserForm(request.POST)

        if form.is_valid(): #2
            new_user = User.objects.create_user(**form.cleaned_data) #5
            
            if user_type == "staff":
                new_user.is_staff = True
                new_user.save()
            
            login(request, new_user)
            return redirect('home')
        else:
            messages.error(request, "Error")
    else:
        # method가 get 일 때
        pass
    return render(request, "signup.html")