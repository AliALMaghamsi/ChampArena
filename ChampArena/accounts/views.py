from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, LoginForm, ProfileEditForm
from django.http import HttpRequest,HttpResponse
from payment.models import Payment
from django.db.models import Sum

def register(request:HttpRequest):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request:HttpRequest):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('accounts:profile')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request:HttpRequest):
    logout(request)
    return redirect('accounts:login')

@login_required
def profile(request:HttpRequest):
    wallet_balance = Payment.objects.filter(user=request.user, status="Succeeded").aggregate(total=Sum('amount'))['total'] or 0
    return render(request, 'accounts/profile.html' , {'wallet_balance': wallet_balance,})

@login_required
def edit_profile(request:HttpRequest):
    user_profile = request.user.profile

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
    else:
        form = ProfileEditForm(instance=user_profile)

    return render(request, 'accounts/edit_profile.html', {'form': form})
