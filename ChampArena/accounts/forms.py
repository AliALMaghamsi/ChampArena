from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.forms import AuthenticationForm

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    phone_number = forms.CharField(max_length=15, required=True, label="Phone Number")
    location = forms.CharField(max_length=255, required=True, label="Location")

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name']
        help_texts = {
            'username': None,
            'email': None,
            'first_name': None,
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        phone_number = cleaned_data.get('phone_number')
        location = cleaned_data.get('location')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                phone_number=self.cleaned_data['phone_number'],
                location=self.cleaned_data['location']
            )
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150, label="Username ")
    password = forms.CharField(widget=forms.PasswordInput())

class ProfileEditForm(forms.ModelForm):
    username = forms.CharField(max_length=150, label="Username")
    first_name = forms.CharField(max_length=30, label="First Name")

    class Meta:
        model = Profile
        fields = ['profile_picture', 'phone_number', 'location']
        widgets = {
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'profile-image-input'}),
        }

    def __init__(self, *args, **kwargs):
        profile = kwargs.get('instance')
        user = profile.user
        super().__init__(*args, **kwargs)
        self.fields['username'].initial = user.username
        self.fields['first_name'].initial = user.first_name

    def save(self):
        user = self.instance.user
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.save()
        profile = super().save(commit=False)
        profile.user = user
        profile.save()
        return user