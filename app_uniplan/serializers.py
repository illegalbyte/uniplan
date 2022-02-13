from rest_framework import serializers
from .models import Enrollments

class EnrollmentsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Enrollments
		fields = '__all__'