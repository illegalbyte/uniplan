from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
	path('', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
	path('accounts/signup/', views.SignupView.as_view(), name='signup'),
]
