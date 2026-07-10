from django.contrib import admin
from .models import Patient, Appointment, TestReport

admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(TestReport)