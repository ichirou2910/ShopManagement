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
		if password == password2:
			if User.objects.filter(username = username).exists():
				messages.info(request,'Username taken')
				return redirect('register')
			elif User.objects.filter(email = email).exists():
				messages.info(request,'Email taken')
				return redirect('register')
			else:
				user = User.objects.create_user(username = username, email = email, password = password, password2 = password2)
				user.save();
				print('User created')
				return redirect('login')
		else:
			messages.info(request,'Password not matching')
			return redirect('register')
		return redirect('/')
	else:
		return render(request, 'register.html')

def login(request):
	if request.medthod == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = auth.authenticate(username = username, password = password)
		if user is not None:
			auth.login(request,user)
			return redirect('/')
		else:
			messages.info(request,'Invalid credentials')
			return redirect('login')
	else:
		return render(request, 'login.html')

def logout(request):
	auth.logout(request)
	return redirect('/')
