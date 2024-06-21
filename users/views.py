from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm
from profiles.forms import ProfileForm
from profiles.models import Profile
import logging
from django.utils import timezone
from datetime import timedelta

logger = logging.getLogger(__name__)



def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile_setup')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid credentials')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def home_view(request):
    user = request.user
    country_filter = request.GET.get('country','')
    rank_filter = request.GET.get('rank', '')
    platform_filter = request.GET.get('platform', '')
    print(f"Country filter: {country_filter}")
    print(f"Rank filter: {rank_filter}")
    print(f"Platform filter: {platform_filter}")

    profiles = Profile.objects.all()

    for profile in profiles:
        profile.is_online = profile.last_active and timezone.now() - profile.last_active < timedelta(minutes=5)
        profile.was_recently_online = profile.last_active and timezone.now() - profile.last_active < timedelta(hours=72)
    
    if country_filter:
        profiles = profiles.filter(country=country_filter)
    if rank_filter:
        profiles = profiles.filter(rank=rank_filter)
    if platform_filter:
        profiles = profiles.filter(type=platform_filter)

    print(f"Profiles count: {profiles.count()}")
    for profile in profiles:
        logger.debug(f"Profile {profile.gaming_id} - User Email: {profile.user.email}")

    context = {
        'user_email': user.email,
        'user_rank': user.profile.rank,  # Supposons que 'rank' est un champ dans le modèle Profile
        'user_country': user.profile.country,  # Supposons que 'country' est un champ dans le modèle Profile
        'user_type': user.profile.type,
        'profiles': profiles,
        'country_filter': country_filter,
        'rank_filter': rank_filter,
        'platform_filter': platform_filter,

    }
    return render(request, 'users/home.html', context)



def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile_setup_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'profiles/profile_setup.html', {'form': form})

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirige vers la même page après la sauvegarde
    else:
        form = ProfileForm(instance=request.user.profile)
    
    return render(request, 'profiles/profile_edit.html', {'form': form})