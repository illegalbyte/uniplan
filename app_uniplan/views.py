from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from .forms import CreateUnitForm, SignupForm, StudentProfileForm, CreateAssignmentForm, ScrapeURLForm, MajorSequence, UnitSetForm, UpdateUserForm, ScrapeSequencesForm, ScrapeSequenceForm
from .models import Unit, Enrollments, Assignment, Semester, Course, UnitSet, MajorSequence, MinorSequence, CoreSequence, UnitData, UnitAvailability
from .deakin_scraper import course_scraper
from django.utils import timezone
import json

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


@login_required
def update_profile(request):
	if request.method =='POST':
		user_form = UpdateUserForm(request.POST, instance=request.user)
		profile_form = StudentProfileForm(request.POST, instance=request.user.student_profile)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			return redirect('update_profile')
	else:
		user_form = UpdateUserForm(instance=request.user)
		profile_form = StudentProfileForm(instance=request.user.student_profile)
	context = {'user_form': user_form, 'profile_form': profile_form}
	print(context)
	return render(request, 'registration/edit_profile.html', context)


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
	enrollments = Enrollments.objects.filter(user=request.user)  # units the user is enrolled in

	context = {'units': units, 'unit_form': unit_form, 'enrollments': enrollments}
	return render(request, 'app_uniplan/create_units.html', context)


@login_required
def unit_detail(request, pk):
	unit = Unit.objects.get(pk=pk)
	unit_info = UnitData.objects.get(unit=unit, year=timezone.now().year)
	context = {'unit': unit, 'unit_info': unit_info}
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
	users_course = user.student_profile.course
	possible_majors = MajorSequence.objects.filter(course=users_course)
	id_of_users_major = user.student_profile.major
	users_core_units_list = UnitSet.objects.filter(core_sequence=CoreSequence.objects.get(course=users_course))
	context = {'enrollments': enrollments, 'years': years, 'users_majors': possible_majors, 'users_core_units_list': users_core_units_list, 'id_of_users_major': id_of_users_major, 'semesters': semesters, 'users_course': users_course}
	return render(request, 'app_uniplan/enrollment.html', context)


@login_required
def batch_add_units(request):
	if request.user.is_superuser:
		if request.method == 'POST':
			unitguide_form = ScrapeURLForm(request.POST)
			sequence_form = ScrapeSequencesForm(request.POST)
			if unitguide_form.is_valid():
				URL = unitguide_form.cleaned_data.get('course_guide_url')
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
					# begin creation of UnitData object to store info about assignments, prerequisites, semester availability
					unit_data = course_scraper.unit_scraper(unit['unitguideURL'])
					# crete unit availability entries in db for this unit
					relevant_year = int(unit_data['year_relevant'][0:4]) # FIXME: Relies on the first 4 chars of the string to be the actual year, vulnerable to format discrepancies
					print(unit_data['trimester_availability'])
					for trimester, data in unit_data['trimester_availability'].items():
						burwood, cloud, geelong = False, False, False
						if data['Burwood'] == True:
							burwood = True
						if data['Cloud'] == True:
							cloud = True
						if data['Geelong'] == True:
							geelong = True
						print(f"year: {relevant_year}, index: {trimester}")
						unitavailability_obj = UnitAvailability(
							unit = unit_obj,
							# FIXME: in order to query for future unknown semesters which don't have a unit guide, we could simply reference whether it has been available in the past at the same trimester
							semester=Semester.objects.get(year=relevant_year, index=trimester),
							burwood = burwood,
							cloud = cloud,
							geelong = geelong
						)
						print(f"CREATED \"UNIT_AVAILABILITY\": {unit['unit_code']}: <{relevant_year}> Semester {str(trimester)}")
					unitavailability_obj.save()
					unitdata_obj = UnitData(
						unit = unit_obj,
						unitguide_url = unit['unitguideURL'],
						raw_data = json.dumps(unit_data),
						year = relevant_year,  
						credit_points = float(unit_data['credit_points']),
						eftsl_value = float(unit_data['EFTSL_value']),
						incompatible_units_text = unit_data['incompatible_with'],
						prerequisite_units_text = unit_data['prerequisite'],
						corequisite_units_text=unit_data['corequisite'],
						assignments_json = json.dumps(unit_data['assignments']),
						trimester_availability_json = json.dumps(unit_data['trimester_availability']),
						hurdle_text = unit_data['hurdle'],
					)
					unitdata_obj.save()
					print(f"CREATED UnitData for {unit['unit_code']}: ID {unitdata_obj.id}")
				return redirect('units')
			if sequence_form.is_valid():
				print("sequence form worked \n\n\n")
				pass

		unitguide_form = ScrapeURLForm
		sequence_form = ScrapeSequencesForm
		context = {'unitguide_form': unitguide_form, 'sequence_form': sequence_form}
		return render(request, 'app_uniplan/scrape_deakin.html', context)

@login_required
def sequences(request):
	# BUG: IN ORDER FOR THESE TO WORK, THE UNITS MUST ALREADY EXIST IN THE DATABASE WHICH OCCURS ONLY THROUGH THE SCRAPE_DEAKIN VIEW CURRENTLY

	if request.method == 'POST':
		sequence_url_form = ScrapeSequencesForm(request.POST)
		add_unit_form = UnitSetForm(request.POST)
		if sequence_url_form.is_valid():
			unitguide_data = course_scraper.deakin_handbook_scraper(sequence_url_form.cleaned_data.get('course_guide_url'))
			majors_urls_list = unitguide_data['major_url_list']
			minor_urls_list = unitguide_data['minor_url_list']
			core_units_dict = unitguide_data['core_units_dict']
			# ASSIGN UNITS IN MAJOR SEQUENCE AS A UNITSET ENTRY IN DB
			for major_url in majors_urls_list:
				major_data = course_scraper.sequence_guide_scraper(major_url)
				major_name = major_data['sequence_name']
				unit_set_code = major_data['unit_set_code']
				course_name = major_data['course_name']
				# create a major sequence if doesn't exist
				if not MajorSequence.objects.filter(title=major_name).exists():
					major_sequence = MajorSequence(
						title = major_name,
						unit_set_code = unit_set_code,
						course = Course.objects.get(course_name=course_name),
					)
					major_sequence.save()
					print(f"SAVED MAJOR SEQUENCE: {major_name}")
				else:
					print(f"MAJOR SEQUENCE ALREADY EXISTS: {major_name}")
				# Assign the major's units to the major sequence
				for unit in major_data['sequence_units_list']:
					# create a unitset if doesn't exist
					if not UnitSet.objects.filter(unit=Unit.objects.get(unit_code=unit[0]), major_sequence=MajorSequence.objects.get(title=major_name)).exists():
						unit_set = UnitSet(
							unit = Unit.objects.get(unit_code=unit[0]),
							major_sequence = MajorSequence.objects.get(title=major_name),
						)
						unit_set.save()
						print(f"ASSIGNED UNIT <{unit[0]}> to MAJOR: {major_name}")
			# ASSIGN UNITS IN MINOR SEQUENCE AS A UNITSET ENTRY IN DB
			for minor_url in minor_urls_list:
				minor_data = course_scraper.sequence_guide_scraper(minor_url)
				minor_name = minor_data['sequence_name']
				unit_set_code = minor_data['unit_set_code']
				course_name = minor_data['course_name']
				# create a minor sequence if doesn't exist
				if not MinorSequence.objects.filter(title=minor_name).exists():
					minor_sequence = MinorSequence(
						title = minor_name,
						unit_set_code = unit_set_code,
						course = Course.objects.get(course_name=course_name),
					)
					minor_sequence.save()
					print(f"SAVED MINOR SEQUENCE: {minor_name}")
				else:
					print(f"MINOR SEQUENCE ALREADY EXISTS: {minor_name}")
				# Assign the minor's units to the minor sequence
				for unit in minor_data['sequence_units_list']:
					# create a unitset if doesn't exist
					if not UnitSet.objects.filter(unit=Unit.objects.get(unit_code=unit[0]), minor_sequence=MinorSequence.objects.get(title=minor_name)).exists():
						unit_set = UnitSet(
							unit = Unit.objects.get(unit_code=unit[0]),
							minor_sequence = MinorSequence.objects.get(title=minor_name),
						)
						unit_set.save()
						print(f"ASSIGNED UNIT <{unit[0]}> to MINOR: {minor_name}")
			# ASSIGN CORE UNITS AS A UNITSET ENTRY IN DB
			# create a core sequence if doesn't exist
			relevant_course = Course.objects.get(course_name=unitguide_data['course_name'])
			if not CoreSequence.objects.filter(course=relevant_course).exists():
				core_sequence = CoreSequence(
					course=Course.objects.get(course_name=relevant_course),
				)
				core_sequence.save()
				print(f"SAVED CORE SEQUENCE: {course_name}")

			for core_unit in core_units_dict.values():
				# create a unitset if doesn't exist
				if not UnitSet.objects.filter(unit=Unit.objects.get(unit_code=core_unit['unit_code']), core_sequence=CoreSequence.objects.get(course=relevant_course)).exists():
					unit_set = UnitSet(
						unit = Unit.objects.get(unit_code=core_unit['unit_code']),
						core_sequence=CoreSequence.objects.get(course=relevant_course),
					)
					unit_set.save()
					print(f"ASSIGNED UNIT <{core_unit['unit_code']}> to CORE SEQUENCE for: {relevant_course}")

			return redirect('sequences')
		elif add_unit_form.is_valid():
			# TODO: Manually add a unit (this should be on the unit details page?)
			return redirect('sequences')
	else:
		user = request.user
		enrollments = Enrollments.objects.filter(user=user)
		semesters = Semester.objects.all()
		courses = Course.objects.all()
		majors = MajorSequence.objects.all()
		minors = MinorSequence.objects.all()

		
		add_unit_form = UnitSetForm
		scrape_url_form = ScrapeSequencesForm
		context = {
			'enrollments': enrollments, 
			'courses': courses, 
			'majors': majors, 
			'minors': minors,
			'add_unit_form': add_unit_form,
			'scrape_url_form': scrape_url_form,
			}
	return render(request, 'app_uniplan/sequences.html', context)
