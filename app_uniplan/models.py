from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Student_Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	course = models.ForeignKey('Course', on_delete=models.CASCADE)
	university = models.ForeignKey('University', on_delete=models.CASCADE)
	major = models.ForeignKey('MajorSequence', on_delete=models.CASCADE, null=True, blank=True)

	def __str__(self):
		return str(self.user)
	
class University(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name

class Course(models.Model):
	course_code = models.CharField(max_length=10)
	course_name = models.CharField(max_length=100)

	def __str__(self):
		return self.course_name

class Semester(models.Model):
	year = models.IntegerField()
	index = models.IntegerField(choices=[(1, "1"), (2, "2"), (3, "3")], default=1)
	start_date = models.DateField(null=True, blank=True)
	end_date = models.DateField(null=True, blank=True)
	
	def __str__(self):
		return f"{self.year}-Semester {self.index}"

class Unit(models.Model):
	'''
	the model for a unit (university subject)
	'''
	name = models.CharField(max_length=200)
	unit_code = models.CharField(max_length=10, unique=True, primary_key=True) #BUG: marking this as unique=True means that units with the same unit_code cannot be created
	unitguideURL = models.URLField(blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	created_date = models.DateTimeField(default=timezone.now)
	created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

	def __str__(self):
		return f"{self.unit_code}: {self.name}"

class UnitData(models.Model):
	'''
	the model for a unit's data
	'''
	unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
	unitguide_url = models.URLField(blank=True, null=True)
	raw_data = models.JSONField()
	created_date = models.DateTimeField(default=timezone.now)
	created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
	
	year = models.IntegerField(default=0, validators=[MinValueValidator(2000), MaxValueValidator(2050)])
	credit_points = models.FloatField(default=0)
	eftsl_value = models.FloatField(default=0)
	incompatible_units_text = models.TextField(blank=True, null=True)
	prerequisite_units_text = models.TextField(blank=True, null=True)
	corequisite_units_text = models.TextField(blank=True, null=True)
	assignments_json = models.JSONField(blank=True, null=True)
	hurdle_text = models.TextField(blank=True, null=True)
	trimester_availability = models.ManyToManyField(Semester, blank=True)




	def __str__(self):
		return f"{self.unit.unit_code}: {self.semester}"

class Enrollments(models.Model):
	'''
	the model for an individual user's enrollment in a unit
	'''
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
	semester = models.ForeignKey(Semester, on_delete=models.CASCADE, null=True)
	passed = models.BooleanField(default=False)
	
	def __str__(self):
		return self.user.username + ' ' + self.unit.name

class Assignment(models.Model):
	'''
	the model for an assignment
	'''
	unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
	unit_data = models.ForeignKey(UnitData, on_delete=models.CASCADE, null=True)
	created_by = models.ForeignKey(User, on_delete=models.CASCADE)
	weighting = models.FloatField(help_text="The % weighting of the assignment in the overall grade as a decimal (e.g. 0.5 for 50%)")
	total_marks_available = models.IntegerField(blank=True, null=True, help_text="The total marks available for the assignment")
	title = models.CharField(max_length=200, help_text="The title of the assignment")
	description = models.TextField(blank=True, null=True, help_text="The description of the assignment")
	due_date = models.DateTimeField(blank=True, null=True, help_text="The due date of the assignment")
	status = models.CharField(blank=True, null=True, max_length=15, choices=[(
		'unpublished', 'Unpublished'), ('open', 'Open'), ('closed', 'Closed'), ('graded', 'Graded')], default='open')
	marks = models.IntegerField(blank=True, null=True, help_text="The marks received for the assignment")
	
	def __str__(self):
		return self.title

class CoreSequence(models.Model):
	'''
	the model for a core sequence (mandatory units) for a course
	Note: this is simply the name of the core sequence, not the actual units
	'''
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	
	def __str__(self):
		return self.course.course_name + ' Core Sequence'

class MajorSequence(models.Model):
	'''
	the model for a major sequence for a course
	Note: this is simply the name of the major sequence, not the actual units
	'''
	title = models.CharField(max_length=300, help_text="The title of the major sequence")
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	units = models.ManyToManyField(Unit)
		
	def __str__(self):
		return self.course.course_name + ': ' + self.title

class MinorSequence(models.Model):
	'''
	the model for a minor sequence for a course
	Note: this is simply the name of the minor sequence, not the actual units
	'''
	title = models.CharField(max_length=300, help_text="The title of the minor sequence")
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
		
	def __str__(self):
		return self.title

class UnitSet(models.Model):
	'''
	the model for which maps units to a sequence
	'''
	unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
	core_sequence = models.ForeignKey(CoreSequence, on_delete=models.CASCADE, blank=True, null=True)
	major_sequence = models.ForeignKey(MajorSequence, on_delete=models.CASCADE, blank=True, null=True)
	minor_sequence = models.ForeignKey(MinorSequence, on_delete=models.CASCADE, blank=True, null=True)
	created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

	def __str__(self):
		return self.unit.name + ': ' + self.sequence.title