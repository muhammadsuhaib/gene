from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404,redirect,HttpResponse
from django.db.models import Q
from .forms import UserForm


# Create your views here.

def login_user(request):
	if request.user.is_authenticated:
		return redirect('/ophthalmology/')
	
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return redirect('/ophthalmology/')
			else:
				return render(request, 'account/login.html', {'error_message': 'Your account has been disabled'})
		else:
			return render(request, 'account/login.html', {'error_message': 'Invalid login'})
			
	return render(request, 'account/login.html')
	
def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return redirect('/')