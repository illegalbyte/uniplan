from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Student_Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	course = models.ForeignKey('Course', on_delete=models.CASCADE)
	university = models.ForeignKey('University', on_delete=models.CASCADE)
	
class University(models.Model):
	name = models.CharField(max_length=50)

class Course(models.Model):
	course_code = models.CharField(max_length=10)
	course_name = models.CharField(max_length=100)

class Semester(models.Model):
	year = models.IntegerField()
	index = models.IntegerField(choices=[(1, "1"), (2, "2"), (3, "3")], default=1)
	start_date = models.DateField()
	end_date = models.DateField()
	
	def __str__(self):
		return self.semester_name

class Unit(models.Model):
	'''
	the model for a unit (university subject)
	'''
	name = models.CharField(max_length=200)
	unit_code = models.CharField(max_length=8, unique=True, primary_key=True)
	unitguideURL = models.URLField(blank=True)
	description = models.TextField()
	created_date = models.DateTimeField(default=timezone.now)
	created_by = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.name

class Enrollments(models.Model):
	'''
	the model for an individual user's enrollment in a unit
	'''
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
	
	def __str__(self):
		return self.user.username + ' ' + self.unit.name

class Assignment(models.Model):
	'''
	the model for an assignment
	'''
	unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
	created_by = models.ForeignKey(User, on_delete=models.CASCADE)
	weighting = models.FloatField(help_text="The % weighting of the assignment in the overall grade as a decimal (e.g. 0.5 for 50%)")
	total_marks_available = models.IntegerField(help_text="The total marks available for the assignment")
	title = models.CharField(max_length=200, help_text="The title of the assignment")
	description = models.TextField(blank=True, null=True, help_text="The description of the assignment")
	due_date = models.DateField()
	
	def __str__(self):
		return self.title