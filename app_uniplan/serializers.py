from rest_framework import serializers
from .models import Enrollments
from rest_framework.fields import CurrentUserDefault

class EnrollmentsSerializer(serializers.ModelSerializer):

	class Meta:
		model = Enrollments
		fields = '__all__'

