from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Unit(models.Model):
	'''
	the model for a unit
	'''
	name = models.CharField(max_length=200)
	unit_code = models.CharField(max_length=8, unique=True, primary_key=True)
	unitguideURL = models.URLField(blank=True)
	description = models.TextField()
	created_date = models.DateTimeField(default=timezone.now)
	created_by = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.name