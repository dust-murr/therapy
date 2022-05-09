from django.contrib import admin
from .models import Therapist, Patient, Appointment, Discharge

class TherapistAdmin(admin.ModelAdmin):
    pass
admin.site.register(Therapist, TherapistAdmin)

class PatientAdmin(admin.ModelAdmin):
    pass
admin.site.register(Patient, PatientAdmin)

class AppointmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Appointment, AppointmentAdmin)

class DischargeAdmin(admin.ModelAdmin):
    pass
admin.site.register(Discharge, DischargeAdmin)
