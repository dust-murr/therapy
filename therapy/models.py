from django.db import models
from django.contrib.auth.models import User

departments = [
    ('Physical Therapy', 'Physical Therapy'),
    ('Occupational Therapy', 'Occupational Therapy'),
    ('Speech Therapy', 'Speech Therapy'),
]

class Therapist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=50, choices=departments, default='Physical Therapy')
    phone_number = models.CharField(max_length=20, null=False)
    status = models.BooleanField(default=False)

    def get_id(self):
        return self.user.id

    def get_name(self):
        return self.user.last_name + ", " + self.user.first_name

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " " + "[" + self.department + "]"


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20, null=False)
    symptoms = models.CharField(max_length=100, null=False)
    registerDate = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
    assignedTherapist = models.PositiveIntegerField(null=True)

    def get_id(self):
        return self.user.id

    def get_name(self):
        return self.user.last_name + ", " + self.user.first_name

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " " + "[" + self.symptoms + "]"


class Appointment(models.Model):
    patient_id = models.PositiveIntegerField(null=True)
    therapist_id = models.PositiveIntegerField(null=True)
    patientName = models.CharField(max_length=100, null=True)
    therapistName = models.CharField(max_length=100, null=True)
    appointmentDate = models.DateTimeField(auto_now=False)
    status = models.BooleanField(default=False)


class Discharge(models.Model):
    patient_id = models.PositiveIntegerField(null=True)
    patientName = models.CharField(max_length=100)
    assignedTherapistName = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, null=False)
    symptoms = models.CharField(max_length=100, null=True)
    registerDate = models.DateTimeField(null=False)
    lastVisitDate = models.DateTimeField(null=False)
    visitNumber = models.PositiveIntegerField(null=False)
    copay = models.PositiveIntegerField(null=False)
    treatmentCost = models.PositiveIntegerField(null=False)
    therapistFee = models.PositiveIntegerField(null=False)
    otherCharge = models.PositiveIntegerField(null=False)
    total = models.PositiveIntegerField(null=False)
    status = models.BooleanField(default=False)