from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms import ModelForm, ModelChoiceField
from .models import User
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


User = get_user_model()

class UserSignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2') 

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_admin = False
        if commit:
            user.save()
        return user


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_admin = False
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Your username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Your password'}))

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)


class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    state = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    zip_code = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))
    country = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    card_number = forms.CharField(max_length=16, widget=forms.TextInput(attrs={'class': 'form-control'}))
    card_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    expiry_date = forms.CharField(max_length=5, widget=forms.TextInput(attrs={'class': 'form-control'}))
    cvv = forms.CharField(max_length=3, widget=forms.TextInput(attrs={'class': 'form-control'}))
