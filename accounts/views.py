from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm


def login_view(request):
	# For now render a simple login template; integration with django.contrib.auth can be added.
	return render(request, 'accounts/login.html')


def signup_view(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('accounts:login')
	else:
		form = UserCreationForm()
	return render(request, 'accounts/signup.html', {'form': form})
