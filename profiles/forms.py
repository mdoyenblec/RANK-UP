# users/forms.py

from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['country', 'type', 'rank', 'gaming_id', 'thumbnail']
        widgets = {
            'country': forms.Select(choices=[
                ('France', 'France'),
                ('Belgium', 'Belgium'),
                ('UK', 'UK'),
                ('Spain','Spain'),
                ('Germany','Germany'),
                ('Italy','Italy'),
                ('Greece','Greece'),
            ], attrs={'class': 'form-control'}),
            'type': forms.Select(choices=[
                ('PS4/PS5', 'PS4/PS5'),
                ('XBOX', 'XBOX'),
                ('PC', 'PC'),
            ], attrs={'class': 'form-control'}),
            'rank': forms.Select(choices=[
                ('Bronze', 'Bronze'),
                ('Silver', 'Silver'),
                ('Gold', 'Gold'),
                ('Platinum', 'Platinum'),
                ('Diamond', 'Diamond'),
                ('Master', 'Master'),
                ('Predator', 'Predator'),
            ], attrs={'class': 'form-control'}),
            'gaming_id': forms.TextInput(attrs={'class': 'form-control'}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
    

        
