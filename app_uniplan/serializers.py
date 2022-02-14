from rest_framework import serializers
from .models import Enrollments, Assignment
from rest_framework.fields import CurrentUserDefault

class EnrollmentsSerializer(serializers.ModelSerializer):

	class Meta:
		model = Enrollments
		fields = '__all__'

class AssignmentSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Assignment
		fields = '__all__'

