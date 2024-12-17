from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, LoginForm, ProfileEditForm
from django.contrib.auth.models import User
from activities.models import Activity
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect('accounts:login')

    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('accounts:profile')
          
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('accounts:login')


@login_required
def profile(request):
    user_profile = request.user.profile
    activities = Activity.objects.filter(created_by=request.user).order_by('-created_at')

    return render(request, 'accounts/profile.html', {
        'user': request.user,
        'wallet_balance': user_profile.wallet_balance,
        'activities': activities
    })

@login_required
def edit_profile(request):
    user_profile = request.user.profile
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
    else:
        form = ProfileEditForm(instance=user_profile)
    return render(request, 'accounts/edit_profile.html', {'form': form})

def host_profile(request, host_id):
    host = get_object_or_404(User, pk=host_id)
    activities = Activity.objects.filter(created_by=host).order_by('-created_at')

    return render(request, 'accounts/host_profile.html', {
        'host': host,
        'profile': host.profile,
        'activities': activities
    })