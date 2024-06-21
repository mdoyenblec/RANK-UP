from django.urls import path
from .views import register_view, login_view, home_view, logout_view, profile_setup_view, profile_edit

urlpatterns = [
    path('register/', register_view, name='register'),
    path('', login_view, name='login'),
    path('home/', home_view, name='home'),
    path('logout/', logout_view, name='logout'),
    path('profile_setup/', profile_setup_view, name='profile_setup'),
    path('profile/edit/', profile_edit, name='profile_edit'),
]
