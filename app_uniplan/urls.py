from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
	path('', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
	path('accounts/signup/', views.signup, name='signup'),
	path('accounts/update_profile/', views.UpdateProfile.as_view(), name='update_profile'),
	path('units/', views.create_units, name='units'),
	path('units/<str:pk>/', views.unit_detail, name='unit_detail'),
	path('assignments/', views.assignments, name='assignments'),
	path('enrollment/', views.enrollment, name='enrollment'),
	path('scrape/', views.batch_add_units, name='scrape'),
	path('sequences/', views.sequences, name='sequences'),
]
