from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
	path('', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
	path('accounts/signup/', views.signup, name='signup'),
	path('accounts/update_profile/', views.update_profile, name='update_profile'),
	path('units/', views.create_units, name='units'),
	path('units/<str:pk>/', views.unit_detail, name='unit_detail'),
	path('assignments/', views.assignments, name='assignments'),
	path('assignments/addallmissing', views.add_all_missing_assignments, name='add_all_missing_assignments'),
	path('enrollment/', views.enrollment, name='enrollment'),
	path('scrape/', views.batch_add_units, name='scrape'),
	path('sequences/', views.sequences, name='sequences'),
	# API URLS
	path('api/enroll/', views.enrollment_get_api, name='enroll_unit_api'),
	path('api/enroll/delete/<str:pk>/', views.enrollment_delete_api, name='delete_enrollment_api'),
	path('api/assignments/', views.AssignmentsAPI.as_view(), name='assignment_api'),

]
