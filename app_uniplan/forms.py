from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

class LoginForm(AuthenticationForm):
	email = forms.forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
	password = forms.CharField(, max_length=, required=False)