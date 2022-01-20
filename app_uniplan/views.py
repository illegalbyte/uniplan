from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.urls import reverse_lazy
from django.views import generic
from .forms import SignupForm, UpdateProfile

# Create your views here.

def index(request):
	return render(request, 'app_uniplan/index.html')

class SignupView(generic.CreateView):
	form_class = SignupForm
	success_url = reverse_lazy('login')
	template_name = 'registration/signup.html'


class UpdateProfile(generic.UpdateView):
	form_class = UpdateProfile
	success_url = reverse_lazy('index')
	template_name = 'registration/edit_profile.html'

	def get_object(self):
		return self.request.user
