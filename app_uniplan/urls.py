from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
	path('', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
	path('accounts/signup/', views.signup, name='signup'),
	path('accounts/update_profile/', views.UpdateProfile.as_view(), name='update_profile'),
]
