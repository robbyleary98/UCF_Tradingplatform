from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from FA_overview.forms import SignUpForm
from django.http import JsonResponse


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in ")
            return redirect('home')
        else:
            messages.success(request, "You cant even remember your password?!")
            return render(request, 'login.html')

    else:

        return render(request, 'login.html')


def logout_user(request):
    logout(request)
    messages.success(request, ("You Have Been Logged Out! Thank You for Visiting :)"))
    return redirect('home')


def register(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password='password')
            login(request, user)
            messages.success(request, ("Yay You Have Registered!"))
            return redirect('home')
        else:
            messages.success(request, ("Oh noo, plz try again!"))
            return redirect('register')
    else:
        return render(request, 'register.html', {'form': form})
