from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.conf import settings
from .forms import RegisterForm, LoginForm
from profiles.forms import ProfileForm
from profiles.models import Profile
from django.utils import timezone
from datetime import timedelta
import logging
import requests
import time



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
        apex_data = get_apex_data(profile.gaming_id, profile.type)
        if apex_data:
            profile.apex_data = apex_data

    context = {
        'user_email': user.email,
        'user_rank': user.profile.rank,  
        'user_country': user.profile.country,  
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





## API Apex Legends Status ##


def map_platform(type):
    platform_mapping = {
        'PS4': 'PS4',
        'XBOX': 'X1',
        'PC': 'PC'
    }
    return platform_mapping.get(type, type)


def get_apex_data(gaming_id, type):
    mapped_platform = map_platform(type)
    cache_key = f"apex_data_{gaming_id}_{mapped_platform}"
    apex_data = cache.get(cache_key)
    if apex_data is None:
        url = f"https://api.mozambiquehe.re/bridge?auth={settings.APEX_API_KEY}&player={gaming_id}&platform={mapped_platform}"
        response = requests.get(url)
        logger.debug(f"Requesting URL: {url}")
        if response.status_code == 200:
            data = response.json()
            if 'global' in data and 'rank' in data['global']:
                apex_data = data['global']['rank']
                logger.debug(f"API Response: {apex_data}")
                cache.set(cache_key, apex_data, timeout=3600)  # Cache for 1 hour
            else:
                apex_data = None
        else:
            logger.error(f"Failed to get data from API. Status code: {response.status_code}, Response: {response.text}")
            apex_data = None
        # Wait 0.5 seconds between requests to not exceed 2 requests per second
        time.sleep(0.5)
    return apex_data

