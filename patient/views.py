from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Patient, Appointment, TestReport
from .forms import PatientForm, AppointmentForm, TestReportForm


# ------------------ Helper ------------------

def is_admin(user):
    return user.is_authenticated and user.is_staff


# ------------------ Public ------------------

def home(request):
    return render(request, 'home.html')


def patient_login(request):
    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:

            login(request, user)

            if user.is_staff:
                return redirect("/admin-dashboard/")
            else:
                return redirect("/patient-dashboard/")

        else:
            messages.error(request, "Invalid Username or Password")

    return render(request, "login.html")


def logout_user(request):
    logout(request)
    return redirect("/")


# ------------------ Admin ------------------

@login_required
@user_passes_test(is_admin)
def dashboard(request):

    context = {
        "patient_count": Patient.objects.count(),
        "appointment_count": Appointment.objects.count(),
        "report_count": TestReport.objects.count(),
        "recent_appointments": Appointment.objects.all().order_by("-created_at")[:5],
        "recent_reports": TestReport.objects.all().order_by("-created_at")[:5],
    }

    return render(request, "dashboard.html", context)


@login_required
@user_passes_test(is_admin)
def register(request):

    if request.method == "POST":

        form = PatientForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            if User.objects.filter(username=username).exists():

                messages.error(request, "Username already exists")
                return render(request, "register.html", {"form": form})

            user = User.objects.create_user(
                username=username,
                password=password
            )

            patient = form.save(commit=False)
            patient.user = user
            patient.save()

            messages.success(request, "Patient Registered Successfully")

            return redirect("/admin-dashboard/")

    else:

        form = PatientForm()

    return render(request, "register.html", {"form": form})


@login_required
@user_passes_test(is_admin)
def search_patient(request):

    patients = []

    if request.method == "POST":

        name = request.POST.get("name")

        patients = Patient.objects.filter(name__icontains=name)

    return render(
        request,
        "search_patient.html",
        {"patients": patients}
    )


@login_required
@user_passes_test(is_admin)
def report(request):

    if request.method == "POST":

        form = TestReportForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            messages.success(request, "Report Uploaded Successfully")

            return redirect("/admin-dashboard/")

    else:

        form = TestReportForm()

    return render(
        request,
        "report.html",
        {"form": form}
    )
# ------------------ Patient ------------------

@login_required
def patient_dashboard(request):

    if request.user.is_staff:
        return redirect("/admin-dashboard/")

    patient = Patient.objects.filter(user=request.user).first()

    if patient is None:
        messages.error(request, "Patient profile not found.")
        return redirect("/logout/")

    appointments = Appointment.objects.filter(
        patient=patient
    ).order_by("-created_at")

    reports = TestReport.objects.filter(
        patient=patient
    ).order_by("-created_at")

    context = {
        "patient": patient,
        "appointments": appointments,
        "reports": reports,
    }

    return render(request, "patient_dashboard.html", context)


@login_required
def appointment(request):

    if request.user.is_staff:
        return redirect("/admin-dashboard/")

    patient = Patient.objects.filter(user=request.user).first()

    if patient is None:
        messages.error(request, "Patient profile not found.")
        return redirect("/patient-dashboard/")

    if request.method == "POST":

        form = AppointmentForm(request.POST)

        if form.is_valid():

            appointment = form.save(commit=False)
            appointment.patient = patient
            appointment.save()

            messages.success(
                request,
                "Appointment Booked Successfully!"
            )

            return redirect("/patient-dashboard/")

    else:

        form = AppointmentForm()

    return render(
        request,
        "appointment.html",
        {
            "form": form
        }
    )
@login_required
@user_passes_test(is_admin)
def approve_appointment(request, id):

    appointment = Appointment.objects.get(id=id)
    appointment.status = "approved"
    appointment.save()

    messages.success(request, "Appointment Approved!")

    return redirect("/admin-dashboard/")


@login_required
@user_passes_test(is_admin)
def reject_appointment(request, id):

    appointment = Appointment.objects.get(id=id)
    appointment.status = "rejected"
    appointment.save()

    messages.success(request, "Appointment Rejected!")

    return redirect("/admin-dashboard/")