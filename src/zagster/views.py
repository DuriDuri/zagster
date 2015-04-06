from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from accounts.forms import RegisterForm
from accounts.models import MyUser

def home(request):
	context = {
		"the_name": 6,
	}
	return render(request, "home.html", context) 

def register(request):
	form = RegisterForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data['username']
		email = form.cleaned_data['email']
		password = form.cleaned_data['password2']
		phone_number = form.cleaned_data['phone_number']
		new_user = MyUser()
		new_user.username = username
		new_user.email = email
		new_user.set_password(password) 
		new_user.phone_number = phone_number
		new_user.save()

		#Test
		all_entries = MyUser.objects.all()
		print all_entries
		return redirect('/')

	context = {
		"form": form,
		"action_value": '',
		"submit_btn_value" : 'Register',
	}
	return render(request, "register.html", context) 