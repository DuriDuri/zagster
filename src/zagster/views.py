from twilio.rest import TwilioRestClient
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from accounts.forms import RegisterForm
from accounts.models import MyUser
from .settings import TWILIO_AUTH_TOKEN, TWILIO_ACCOUNT_SID
from .task_form import TaskForm

def home(request):
	taskform = TaskForm(request.POST or None)
	if taskform.is_valid():
		print 'Button Pressed'
		data = taskform.cleaned_data
		client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

		#Load all users 
		all_users = MyUser.objects.all()
		for user in all_users:
			recepient = "+1%s" % (user.phone_number)
			message = "Hey %s! \n new offer just in: \n From: %s \n Task: %s \n For: $%s" % (user.first_name, data['requestor'], data['task'], data['offer'])
			print recepient + message
			message = client.messages.create(body=message,
				to=recepient,
				from_="+12404828017")



	context = {
		"taskform": taskform,
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