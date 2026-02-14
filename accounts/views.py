from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import SignupForm, LoginForm, ProfileForm
from django.contrib.auth import login, logout
from django.urls import reverse
from django.shortcuts import resolve_url


def login_view(request):
	if request.method == 'POST':
		form = LoginForm(request.POST, request=request)
		if form.is_valid():
			user = form.cleaned_data.get('user')
			login(request, user)
			# redirect 'Comum' users to their tickets list
			if getattr(user, 'typeUser', None) == 'Comum':
				return redirect('tickets:my_tickets')
			return redirect('core:home')
	else:
		form = LoginForm()
	return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
	logout(request)
	return redirect('accounts:login')


def signup_view(request):
	if request.method == 'POST':
		form = SignupForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return redirect('accounts:login')
	else:
		form = SignupForm()
	return render(request, 'accounts/signup.html', {'form': form})


@login_required
def profile_view(request):
	user = request.user
	if request.method == 'POST':
		form = ProfileForm(request.POST, request.FILES, instance=user)
		if form.is_valid():
			form.save()
			messages.success(request, 'Perfil atualizado com sucesso.')
			return redirect('accounts:profile')
	else:
		form = ProfileForm(instance=user)
	return render(request, 'accounts/profile.html', {'form': form, 'user_obj': user})
