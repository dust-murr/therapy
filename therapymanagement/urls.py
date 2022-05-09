from django.contrib import admin
from django.urls import path
from therapy import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name=''),
    path('admin', views.admin),
    path('therapist', views.therapist),
    path('patient', views.patient),
    path('about', views.about),
    path('contact', views.contact),
    path('adminregister', views.admin_register),
    path('therapistregister', views.therapist_register),
    path('patientregister', views.patient_register),
    path('adminlogin', LoginView.as_view(template_name='therapy/adminlogin.html')),
    path('therapistlogin', LoginView.as_view(template_name='therapy/therapistlogin.html')),
    path('patientlogin', LoginView.as_view(template_name='therapy/patientlogin.html')),
    path('logged-in', views.logged_in_view, name='logged-in'),
    path('logged-out', LogoutView.as_view(template_name='therapy/homepage.html'), name='logged-out'),


# ADMIN URLs
    path('admin-page', views.admin_page, name='admin-page'),
    path('admin-therapist', views.admin_therapist_view, name='admin-therapist'),
    path('admin-therapist-record', views.admin_therapist_record_view, name='admin-therapist-record'),
    path('delete-therapist/<int:pk>', views.delete_therapist_view, name='delete-therapist'),
    path('update-therapist/<int:pk>', views.update_therapist_view, name='update-therapist'),
    path('admin-register-therapist', views.admin_register_therapist_view, name='admin-register-therapist'),
    path('admin-approve-therapist', views.admin_approve_therapist_view, name='admin-approve-therapist'),
    path('approve-therapist/<int:pk>', views.approve_therapist_view, name='approve-therapist'),
    path('reject-therapist/<int:pk>', views.reject_therapist_view, name='reject-therapist'),
    path('admin-therapist-department', views.admin_therapist_department_view, name='admin-therapist-department'),
    path('admin-patient', views.admin_patient_view, name='admin-patient'),
    path('admin-patient-record', views.admin_patient_record_view, name='admin-patient-record'),
    path('delete-patient/<int:pk>', views.delete_patient_view, name='delete-patient'),
    path('update-patient/<int:pk>', views.update_patient_view, name='update-patient'),
    path('admin-register-patient', views.admin_register_patient_view, name='admin-register-patient'),
    path('admin-approve-patient', views.admin_approve_patient_view, name='admin-approve-patient'),
    path('approve-patient/<int:pk>', views.approve_patient_view, name='approve-patient'),
    path('reject-patient/<int:pk>', views.reject_patient_view, name='reject-patient'),
    path('admin-discharge-patient', views.admin_discharge_patient_view, name='admin-discharge-patient'),
    path('discharge-patient/<int:pk>', views.discharge_patient_view, name='discharge-patient'),
    path('download-pdf/<int:pk>', views.download_pdf_view, name='download-pdf'),
    path('admin-appointment', views.admin_appointment_view, name='admin-appointment'),
    path('admin-appointment-record', views.admin_appointment_record_view, name='admin-appointment-record'),
    path('delete-admin-appointment/<int:pk>', views.delete_admin_appointment_view, name='delete-admin-appointment'),
    path('update-admin-appointment/<int:pk>', views.update_admin_appointment_view, name='update-admin-appointment'),
    path('admin-add-appointment', views.admin_add_appointment_view, name='admin-add-appointment'),
    path('admin-approve-appointment', views.admin_approve_appointment_view, name='admin-approve-appointment'),
    path('approve-appointment/<int:pk>', views.approve_appointment_view, name='approve-appointment'),
    path('reject-appointment/<int:pk>', views.reject_appointment_view, name='reject-appointment'),
]

# THERAPIST URLs
urlpatterns += [
    path('therapist-page', views.therapist_page_view, name='therapist-page'),
    path('therapist-patient', views.therapist_patient_view, name='therapist-patient'),
    path('therapist-patient-record', views.therapist_patient_record_view, name='therapist-patient-record'),
    path('therapist-discharge-patient', views.therapist_discharge_patient_view, name='therapist-discharge-patient'),
    path('therapist-appointment-record', views.therapist_appointment_record_view, name='therapist-appointment-record'),
    path('delete-appointment/<int:pk>', views.delete_appointment_view, name='delete-appointment'),
]

# PATIENT URLs
urlpatterns += [
    path('patient-page', views.patient_page_view, name='patient-page'),
    path('patient-appointment', views.patient_appointment_view, name='patient-appointment'),
    path('patient-book-appointment', views.patient_book_appointment_view, name='patient-book-appointment'),
    path('patient-appointment-record', views.patient_appointment_record_view, name='patient-appointment-record'),
    path('patient-therapist-record', views.patient_therapist_record_view, name='patient-therapist-record'),
    path('patient-discharge', views.patient_discharge_view, name='patient-discharge'),
]