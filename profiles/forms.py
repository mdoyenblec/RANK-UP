from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['country', 'platform', 'gaming_id', 'thumbnail', 'your_bio']
        widgets = {
            'country': forms.Select(choices=[
                ('France', 'France'),
                ('Belgium', 'Belgium'),
                ('UK', 'UK'),
                ('Spain','Spain'),
                ('Germany','Germany'),
                ('Italy','Italy'),
                ('Greece','Greece'),
            ], attrs={'class': 'form-select'}),
            'platform': forms.Select(choices=[
                ('PS4', 'PS4'),
                ('X1', 'XBOX'),
                ('PC', 'PC'),
            ], attrs={'class': 'form-select'}),
            'gaming_id': forms.TextInput(attrs={'class': 'form-control'}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'your_bio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Looking for ...'}),
        }
