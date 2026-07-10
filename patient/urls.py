from django.urls import path
from . import views

urlpatterns = [
    # Public
    path('', views.home, name='home'),
    path('login/', views.patient_login, name='login'),
    path('logout/', views.logout_user, name='logout'),

    # Admin
    path('admin-dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('search-patient/', views.search_patient, name='search_patient'),
    path('report/', views.report, name='report'),
    path('approve/<int:id>/', views.approve_appointment, name='approve'),
    path('reject/<int:id>/', views.reject_appointment, name='reject'),


    # Patient
    path('patient-dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('appointment/', views.appointment, name='appointment'),
]