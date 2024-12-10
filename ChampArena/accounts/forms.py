from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")
    location = forms.CharField(max_length=255, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            location = self.cleaned_data['location']
            profile = Profile.objects.create(user=user, location=location)
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150, label="Username ")
    password = forms.CharField(widget=forms.PasswordInput())

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'wallet_balance', 'phone_number', 'location']
        widgets = {
            'profile_picture': forms.ClearableFileInput(),
        }
