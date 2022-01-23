from pprint import pprint
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from .forms import CreateUnitForm, SignupForm, UpdateProfile, StudentProfileForm, CreateAssignmentForm, ScrapeURLForm
from .models import Unit, Student_Profile, Enrollments, Assignment, Semester
from .deakin_scraper import course_scraper

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


@login_required
def create_units(request):
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


@login_required
def unit_detail(request, pk):
	unit = Unit.objects.get(pk=pk)
	context = {'unit': unit}
	return render(request, 'app_uniplan/unit_detail.html', context)


@login_required
def assignments(request):
	add_assignment_form = CreateAssignmentForm
	user = request.user
	assignments = Assignment.objects.filter(created_by=user)
	context = {'assignments': assignments, 'form': add_assignment_form}
	return render(request, 'app_uniplan/assignments.html', context)


@login_required
def enrollment(request):
	years = Semester.objects.all().order_by('year').values_list('year', flat=True).distinct()
	user = request.user
	enrollments = Enrollments.objects.filter(user=user)
	semesters = Semester.objects.all()
	context = {'enrollments': enrollments, 'years': years}
	return render(request, 'app_uniplan/enrollment.html', context)


@login_required
def batch_add_units(request):
	if request.user.is_superuser:
		if request.method == 'POST':
			form = ScrapeURLForm(request.POST)
			if form.is_valid():
				URL = form.cleaned_data.get('course_guide_url')
				print(f"SCRAPING URL: {URL}")
				course_data = course_scraper.deakin_handbook_scraper(URL)
				units = course_data['units'].values()
				for unit in units:
					unit_obj = Unit(
						unit_code = unit['unit_code'],
						name = unit['unit_name'],
						unitguideURL=unit['unitguideURL'],
						created_by = request.user
					)
					unit_obj.save()
					print(f"SAVED UNIT: {unit['unit_code']}: {unit['unit_name']}")
				return redirect('units')
		form = ScrapeURLForm
		context = {'form': form}
		return render(request, 'app_uniplan/scrape_deakin.html', context)
