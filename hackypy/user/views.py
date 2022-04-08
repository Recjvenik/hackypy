from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import UserForm
from django.contrib.auth import authenticate, login, logout


def loginUser(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "user does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "username OR password is incorrect")
    
    return render(request, 'user/login_register.jinja')


def registerUser(request):

    page = 'register'

    form = UserForm()

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "An error has occured, try again later")

    context = {
        'form':form, 'page':page
    }

    return render(request, 'user/login_register.jinja', context)


def logoutUser(request):
    logout(request)
    return redirect ('login')

        