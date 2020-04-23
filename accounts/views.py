from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages

# Create your views here.


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        redirect_url = request.GET.get('next', '')
        # If password is correct
        if password == password2:
            # If the username exists
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username taken, please use another one.')
                return redirect('register')
            # If the email exists
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email taken already, please use another one.')
                return redirect('register')
            # Create new user and redirect
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            if not redirect_url:
                return redirect('/')
            return redirect(redirect_url)
        messages.info(request, 'Password not matching, please try again.')
        return redirect('register')
    return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        redirect_url = request.GET.get('next', '')
        user = auth.authenticate(username=username, password=password)
        # If login successfully
        if user is not None:
            auth.login(request, user)
            if not redirect_url:
                return redirect('/')
            return redirect(redirect_url)
        messages.info(request, 'Invalid credentials, please try again')
        return redirect('login')
    return render(request, 'login.html')


def logout(request):
    redirect_url = request.GET.get('next', '')
    auth.logout(request)
    if not redirect_url:
        return redirect('/')
    return redirect(redirect_url)
