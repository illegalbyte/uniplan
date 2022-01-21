from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.urls import reverse_lazy
from django.views import generic
from .forms import CreateUnitForm, SignupForm, UpdateProfile, StudentProfileForm
from .models import Unit, Student_Profile, Enrollments, Assignment

# Create your views here.

def index(request):
	return render(request, 'app_uniplan/index.html')

def signup(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		profile_form = StudentProfileForm(request.POST)
		
		if form.is_valid() and profile_form.is_valid():
			user = form.save()

			profile = profile_form.save(commit=False)
			profile.user = user
			profile.save()

			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('index')
	else:
		form = SignupForm()
		profile_form = StudentProfileForm()
	return render(request, 'registration/signup.html', {'form': form, 'profile_form': profile_form})


class UpdateProfile(generic.UpdateView):
	form_class = UpdateProfile
	success_url = reverse_lazy('index')
	template_name = 'registration/edit_profile.html'

	def get_object(self):
		return self.request.user

def create_units(request):
	if not request.user.is_authenticated:
		return redirect('login')
	
	if request.method == 'POST':
		form = CreateUnitForm(request.POST)
		if form.is_valid():
			unit = form.save(commit=False)
			unit.created_by = request.user
			unit.save()
			return redirect('units')

	unit_form = CreateUnitForm
	units = Unit.objects.all()
	context = {'units': units, 'unit_form': unit_form}
	return render(request, 'app_uniplan/create_units.html', context)

def unit_detail(request, pk):
	if not request.user.is_authenticated:
		return redirect('login')
	unit = Unit.objects.get(pk=pk)
	context = {'unit': unit}
	return render(request, 'app_uniplan/unit_detail.html', context)

def assignments(request):
	if not request.user.is_authenticated:
		return redirect('login')

	user = request.user
	assignments = Assignment.objects.filter(created_by=user)
	context = {'assignments': assignments}
	return render(request, 'app_uniplan/assignments.html', context)