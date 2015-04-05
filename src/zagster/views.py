from django.shortcuts import render
from django.http import HttpResponseRedirect

from accounts.forms import RegisterForm

def home(request):
	context = {
		"the_name": 6,
	}
	return render(request, "home.html", context) 