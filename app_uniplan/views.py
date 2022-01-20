from django.shortcuts import render
from django.contrib.auth.views import LoginView


# Create your views here.

def index(request):
	return render(request, 'app_uniplan/index.html')

class CustomLoginView(LoginView):
	login_template = 'app_uniplan/login.html'
	def form_valid(self, form):
		return super(CustomLoginView, self).form_valid(form)