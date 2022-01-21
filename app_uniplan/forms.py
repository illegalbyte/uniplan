from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import *

class SignupForm(UserCreationForm):	
	bootstrap_attributes = 'form-control'

	username = forms.CharField(max_length=30, required=True, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', label='Username', widget=forms.TextInput(attrs={'class': bootstrap_attributes}))
	email = forms.EmailField(max_length=200, help_text='Required', widget=forms.EmailInput(attrs={'class':bootstrap_attributes}))
	first_name = forms.CharField(max_length=25, help_text='Required', widget=forms.TextInput(attrs={'class':bootstrap_attributes}))
	last_name = forms.CharField(max_length=25, help_text='Required', widget=forms.TextInput(attrs={'class':bootstrap_attributes}))
	password1 = forms.CharField(max_length=30, required=True, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', label='Password', widget=forms.PasswordInput(attrs={'class':bootstrap_attributes}))
	password2 = forms.CharField(max_length=30, required=True, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', label='Password Confirmation', widget=forms.PasswordInput(attrs={'class': bootstrap_attributes}))

	class Meta:
		model = User
		fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')


class StudentProfileForm(forms.ModelForm):
	bootstrap_attributes = 'form-control'

	course = forms.ModelChoiceField(required=True, queryset=Course.objects.all(
	), widget=forms.Select(attrs={'class': bootstrap_attributes}))
	university = forms.ModelChoiceField(required=True, queryset=University.objects.all(
	), widget=forms.Select(attrs={'class': bootstrap_attributes}))
	
	class Meta:
		model = Student_Profile
		fields = ('course', 'university')

class UpdateProfile(UserChangeForm):
	bootstrap_attributes = 'form-control'

	username = forms.CharField(max_length=30, required=True, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', label='Username', widget=forms.TextInput(attrs={'class': bootstrap_attributes}))
	email = forms.EmailField(max_length=200, widget=forms.EmailInput(attrs={'class': bootstrap_attributes}))
	first_name = forms.CharField(max_length=25, widget=forms.TextInput(attrs={'class': bootstrap_attributes}))
	last_name = forms.CharField(max_length=25, widget=forms.TextInput(attrs={'class': bootstrap_attributes}))
	password = None

	class Meta:
		model = User
		fields = ('username', 'email', 'first_name','last_name')

#TODO: Add a form for the student profile which will be used to update the student profile.

class CreateUnitForm(forms.ModelForm):
	name = forms.CharField(max_length=80, required=True, help_text='Required. 50 characters or fewer.', label='Unit Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
	unit_code = forms.CharField(max_length=10, required=True, help_text='Required. 10 characters or fewer.', label='Unit Code', widget=forms.TextInput(attrs={'class': 'form-control'}))
	description = forms.CharField(max_length=200, required=False, help_text='Unit Description.', label='Unit Description', widget=forms.Textarea(attrs={'class': 'form-control'}))
	unitguideURL = forms.URLField(max_length=300, required=False, help_text='Unit Guide URL.', label='Unit Guide URL', widget=forms.URLInput(attrs={'class': 'form-control'}))

	class Meta:
		model = Unit
		fields = ('name', 'unit_code', 'description', 'unitguideURL')

class CreateAssignmentForm(forms.ModelForm):
	bootstrap_attributes = 'form-control'

	class Meta:
		model = Assignment
		fields = '__all__'
		exclude = ['created_by']
