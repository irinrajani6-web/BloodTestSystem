from django import forms
from .models import Patient, Appointment, TestReport


class PatientForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Patient
        fields = [
            'name',
            'email',
            'age',
            'gender',
            'contact',
        ]


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [
            'date',
            'time',
            'reason',
        ]

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'reason': forms.Textarea(attrs={'rows': 3}),
        }


class TestReportForm(forms.ModelForm):
    class Meta:
        model = TestReport
        fields = [
            'patient',
            'title',
            'description',
            'file',
        ]