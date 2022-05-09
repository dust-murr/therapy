import datetime

from django import forms
from django.contrib.auth.models import User
from . import models


# Admin form
class AdminUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            'password'
        ]

#------------------------------------------------------------------------------------------------

# Therapist form
class TherapistUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            'password'
        ]

class TherapistForm(forms.ModelForm):
    class Meta:
        model = models.Therapist
        fields = [
            'phone_number',
            'department',
            'status'
        ]

#------------------------------------------------------------------------------------------------

# Patient form
class PatientUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            'password'
        ]

class PatientForm(forms.ModelForm):
    assignedTherapist = forms.ModelChoiceField(
        queryset=models.Therapist.objects.all().filter(status=True),
        empty_label="Name [Department]",
        to_field_name="user_id"
    )
    class Meta:
        model = models.Patient
        fields = [
            'address',
            'phone_number',
            'symptoms',
            'status'
        ]




#------------------------------------------------------------------------------------------------

# Appointment form
class AppointmentForm(forms.ModelForm):
    therapist_id = forms.ModelChoiceField(
        queryset=models.Therapist.objects.all().filter(status=True),
        empty_label="Therapist Name [Department]",
        to_field_name="user_id"
    )
    patient_id = forms.ModelChoiceField(
        queryset=models.Patient.objects.all().filter(status=True),
        empty_label="Patient Name [Symptoms]",
        to_field_name="user_id"
    )

    appointmentDate = forms.DateTimeField(widget=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'}))

    class DateTimeInput(forms.DateTimeInput):
        input_type = 'datetime-local'

    class Meta:
        model = models.Appointment
        fields = [
            'status'
        ]

class PatientAppointmentForm(forms.ModelForm):
    therapist_id = forms.ModelChoiceField(
        queryset=models.Therapist.objects.all().filter(status=True),
        empty_label="Therapist Name [Department]",
        to_field_name="user_id"
    )
    appointmentDate = forms.DateTimeField(widget=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'}))

    class DateTimeInput(forms.DateTimeInput):
        input_type = 'datetime-local'

    class Meta:
        model = models.Appointment
        fields = [
            'status'
        ]

#------------------------------------------------------------------------------------------------

#Contact form
class ContactForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(
        max_length=500,
        widget=forms.Textarea(attrs={'rows': 3, 'cols': 30})
    )