from datetime import date
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, reverse
import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.http import HttpResponse
from . import models, forms


def home(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('logged-in')
    return render(request, 'therapy/homepage.html')


# About
def about(request):
    return render(request, 'therapy/about.html')


# Contact
def contact(request):
    sub = forms.ContactForm()
    if request.method == 'POST':
        sub = forms.ContactForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name = sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name) + ' || ' + str(email), message, settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER,
                      fail_silently=False)
            return render(request, 'therapy/contact_success.html')
    return render(request, 'therapy/contact.html', {'form': sub})


# Admin login
def admin(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('logged-in')
    return render(request, 'therapy/adminlogin.html')


# Therapist login
def therapist(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('logged-in')
    return render(request, 'therapy/therapistlogin.html')


# Patient login
def patient(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('logged-in')
    return render(request, 'therapy/patientlogin.html')


# Admin register
def admin_register(request):
    userForm = forms.AdminUserForm()
    mydict = {'userForm': userForm}
    if request.method == 'POST':
        userForm = forms.AdminUserForm(request.POST)
        if userForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            admin_group = Group.objects.get_or_create(name='ADMIN')
            admin_group[0].user_set.add(user)
            return HttpResponseRedirect('adminlogin')
    return render(request, 'therapy/adminregister.html', context=mydict)


# Therapist register
def therapist_register(request):
    userForm = forms.TherapistUserForm()
    therapistForm = forms.TherapistForm()
    mydict = {'userForm': userForm, 'therapistForm': therapistForm}
    if request.method == 'POST':
        userForm = forms.TherapistUserForm(request.POST)
        therapistForm = forms.TherapistForm(request.POST, request.FILES)
        if userForm.is_valid() and therapistForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            therapist = therapistForm.save(commit=False)
            therapist.user = user
            therapist = therapist.save()
            therapist_group = Group.objects.get_or_create(name='THERAPIST')
            therapist_group[0].user_set.add(user)
        return HttpResponseRedirect('therapistlogin')
    return render(request, 'therapy/therapistregister.html', context=mydict)


# Patient register
def patient_register(request):
    userForm = forms.PatientUserForm()
    patientForm = forms.PatientForm()
    mydict = {'userForm': userForm, 'patientForm': patientForm}
    if request.method == 'POST':
        userForm = forms.PatientUserForm(request.POST)
        patientForm = forms.PatientForm(request.POST, request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            patient = patientForm.save(commit=False)
            patient.user = user
            patient.assignedTherapist = request.POST.get('assignedTherapist')
            patient = patient.save()
            patient_group = Group.objects.get_or_create(name='PATIENT')
            patient_group[0].user_set.add(user)
        return HttpResponseRedirect('patientlogin')
    return render(request, 'therapy/patientregister.html', context=mydict)


# User Verification
def admin_verified(user):
    return user.groups.filter(name='ADMIN').exists()


def therapist_verified(user):
    return user.groups.filter(name='THERAPIST').exists()


def patient_verified(user):
    return user.groups.filter(name='PATIENT').exists()


# Check username and password of user
def logged_in_view(request):
    if admin_verified(request.user):
        return redirect('admin-page')
    elif therapist_verified(request.user):
        verified = models.Therapist.objects.all().filter(user_id=request.user.id, status=True)
        if verified:
            return redirect('therapist-page')
        else:
            return render(request, 'therapy/therapist_wait.html')
    elif patient_verified(request.user):
        verified = models.Patient.objects.all().filter(user_id=request.user.id, status=True)
        if verified:
            return redirect('patient-page')
        else:
            return render(request, 'therapy/patient_wait.html')


# ADMIN VIEW
@login_required(login_url='adminlogin')
@user_passes_test(admin_verified)
def admin_page(request):
    # for all tables in admin_page
    therapists = models.Therapist.objects.all().order_by('-id')
    patients = models.Patient.objects.all().order_by('-id')
    appointments = models.Appointment.objects.all().order_by('-id')

    # for three cards
    therapist_count = models.Therapist.objects.all().filter(status=True).count()
    pending_therapist = models.Therapist.objects.all().filter(status=False).count()

    patient_count = models.Patient.objects.all().filter(status=True).count()
    pending_patient = models.Patient.objects.all().filter(status=False).count()

    appointment_count = models.Appointment.objects.all().filter(status=True).count()
    pending_appointment = models.Appointment.objects.all().filter(status=False).count()
    mydict = {
        'therapists': therapists,
        'patients': patients,
        'appointments': appointments,
        'therapist_count': therapist_count,
        'pending_therapist': pending_therapist,
        'patient_count': patient_count,
        'pending_patient': pending_patient,
        'appointment_count': appointment_count,
        'pending_appointment': pending_appointment,
    }
    return render(request, 'therapy/admin_page.html', context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(admin_verified)
def admin_therapist_view(request):
    return render(request, 'therapy/admin_therapist.html')


@login_required(login_url='adminlogin')
@user_passes_test(admin_verified)
def admin_therapist_record_view(request):
    therapists = models.Therapist.objects.all().filter(status=True)
    return render(request, 'therapy/admin_therapist_record.html', {'therapists': therapists})


@login_required(login_url='adminlogin')
@user_passes_test(admin_verified)
def delete_therapist_view(request, pk):
    therapist = models.Therapist.objects.get(id=pk)
    user = models.User.objects.get(id=therapist.user_id)
    user.delete()
    therapist.delete()
    return redirect('admin-therapist-record')


@login_required(login_url='adminlogin')
@user_passes_test(admin_verified)
def update_therapist_view(request, pk):
    therapist = models.Therapist.objects.get(id=pk)
    user = models.User.objects.get(id=therapist.user_id)
    userForm = forms.TherapistUserForm(instance=user)
    therapistForm = forms.TherapistForm(request.FILES, instance=therapist)
    mydict = {'userForm': userForm, 'therapistForm': therapistForm}
    if request.method == 'POST':
        userForm = forms.TherapistUserForm(request.POST, instance=user)
        therapistForm = forms.TherapistForm(request.POST, request.FILES, instance=therapist)
        if userForm.is_valid() and therapistForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            therapist = therapistForm.save(commit=False)
            therapist.status = True
            therapist.save()
            return redirect('admin-therapist-record')
    return render(request, 'therapy/admin_update_therapist.html', context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(admin_verified)
def admin_register_therapist_view(request):
    userForm = forms.TherapistUserForm()
    therapistForm = forms.TherapistForm()
    mydict = {'userForm': userForm, 'therapistForm': therapistForm}
    if request.method == 'POST':
        userForm = forms.TherapistUserForm(request.POST)
        therapistForm = forms.TherapistForm(request.POST, request.FILES)
        if userForm.is_valid() and therapistForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            therapist = therapistForm.save(commit=False)
            therapist.user = user
            therapist.status = True
            therapist.save()
            my_therapist_group = Group.objects.get_or_create(name='THERAPIST')
            my_therapist_group[0].user_set.add(user)
        return HttpResponseRedirect('admin-therapist')
    return render(request, 'therapy/admin_register_therapist.html', context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(admin_verified)
def admin_approve_therapist_view(request):
    # those whose approval are needed
    therapists = models.Therapist.objects.all().filter(status=False)
    return render(request, 'therapy/admin_approve_therapist.html', {'therapists': therapists})


@login_required(login_url='adminlogin')
@user_passes_test(admin_verified)
def approve_therapist_view(request, pk):
    therapist = models.Therapist.objects.get(id=pk)
    therapist.status = True
    therapist.save()
    return redirect(reverse('admin-approve-therapist'))


@login_required(login_url='adminlogin')
@user_passes_test(admin_verified)
def reject_therapist_view(request, pk):
    therapist = models.Therapist.objects.get(id=pk)
    user = models.User.objects.get(id=therapist.user_id)
    user.delete()
    therapist.delete()
    return redirect('admin-approve-therapist')


@login_required(login_url='adminlogin')
@user_passes_test(admin_verified)
def admin_therapist_department_view(request):
    therapists = models.Therapist.objects.all().filter(status=True)
    return render(request, 'therapy/admin_therapist_department.html', {'therapists': therapists})


@login_required(login_url='adminlogin')
@user_passes_test(admin_verified)
def admin_patient_view(request):
    return render(request, 'therapy/admin_patient.html')


@login_required(login_url='adminlogin')
@user_passes_test(admin_verified)
def admin_patient_record_view(request):
    patients = models.Patient.objects.all().filter(status=True)
    return render(request, 'therapy/admin_patient_record.html', {'patients': patients})


@login_required(login_url='adminlogin')
@user_passes_test(admin_verified)
def delete_patient_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    user = models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin-patient-record')


@login_required(login_url='adminlogin')
@user_passes_test(admin_verified)
def update_patient_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    user = models.User.objects.get(id=patient.user_id)
    userForm = forms.PatientUserForm(instance=user)
    patientForm = forms.PatientForm(request.FILES, instance=patient)
    mydict = {'userForm': userForm, 'patientForm': patientForm}
    if request.method == 'POST':
        userForm = forms.PatientUserForm(request.POST, instance=user)
        patientForm = forms.PatientForm(request.POST, request.FILES, instance=patient)
        if userForm.is_valid() and patientForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            patient = patientForm.save(commit=False)
            patient.status = True
            patient.assignedTherapist = request.POST.get('assignedTherapist')
            patient.save()
            return redirect('admin-patient-record')
    return render(request, 'therapy/admin_update_patient.html', context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(admin_verified)
def admin_register_patient_view(request):
    userForm = forms.PatientUserForm()
    patientForm = forms.PatientForm()
    mydict = {'userForm': userForm, 'patientForm': patientForm}
    if request.method == 'POST':
        userForm = forms.PatientUserForm(request.POST)
        patientForm = forms.PatientForm(request.POST, request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            patient = patientForm.save(commit=False)
            patient.user = user
            patient.status = True
            patient.assignedTherapist = request.POST.get('assignedTherapist')
            patient.save()
            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
        return HttpResponseRedirect('admin-patient')
    return render(request, 'therapy/admin_register_patient.html', context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(admin_verified)
def admin_approve_patient_view(request):
    # those whose approval are needed
    patients = models.Patient.objects.all().filter(status=False)
    return render(request, 'therapy/admin_approve_patient.html', {'patients': patients})


@login_required(login_url='adminlogin')
@user_passes_test(admin_verified)
def approve_patient_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    patient.status = True
    patient.save()
    return redirect(reverse('admin-approve-patient'))


@login_required(login_url='adminlogin')
@user_passes_test(admin_verified)
def reject_patient_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    user = models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin-approve-patient')


@login_required(login_url='adminlogin')
@user_passes_test(admin_verified)
def admin_discharge_patient_view(request):
    patients = models.Patient.objects.all().filter(status=True)
    return render(request, 'therapy/admin_discharge_patient.html', {'patients': patients})


@login_required(login_url='adminlogin')
@user_passes_test(admin_verified)
def discharge_patient_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    assignedTherapist = models.User.objects.all().filter(id=patient.assignedTherapist)
    patientD = {
        'patient_id': pk,
        'patientName': patient.get_name(),
        'phone_number': patient.phone_number,
        'address': patient.address,
        'symptoms': patient.symptoms,
        'registerDate': patient.registerDate,
        'lastVisitDate': date.today(),
        'assignedTherapistName': assignedTherapist[0].first_name + " " + assignedTherapist[0].last_name,
    }
    if request.method == 'POST':
        fee = {
            'visitNumber': int(request.POST['visitNumber']),
            'copay': int(request.POST['copay']) * int(request.POST['visitNumber']),
            'therapistFee': request.POST['therapistFee'],
            'treatmentCost': request.POST['treatmentCost'],
            'otherCharge': request.POST['otherCharge'],
            'total': (int(request.POST['copay']) * int(request.POST['visitNumber'])) + int(
                request.POST['therapistFee']) + int(request.POST['treatmentCost']) + int(request.POST['otherCharge']),
        }
        patientD.update(fee)
        d = models.Discharge()
        d.patient_id = pk
        d.patientName = patient.get_name()
        d.assignedTherapistName = assignedTherapist[0].first_name + " " + assignedTherapist[0].last_name
        d.address = patient.address
        d.phone_number = patient.phone_number
        d.symptoms = patient.symptoms
        d.registerDate = patient.registerDate
        d.lastVisitDate = date.today()
        d.visitNumber = int(request.POST['visitNumber'])
        d.treatmentCost = int(request.POST['treatmentCost'])
        d.copay = int(request.POST['copay']) * int(request.POST['visitNumber'])
        d.therapistFee = int(request.POST['therapistFee'])
        d.otherCharge = int(request.POST['otherCharge'])
        d.total = (int(request.POST['copay']) * int(request.POST['visitNumber'])) + int(
            request.POST['therapistFee']) + int(request.POST['treatmentCost']) + int(request.POST['otherCharge'])
        d.status = True
        d.save()
        return render(request, 'therapy/final_bill.html', context=patientD)
    return render(request, 'therapy/create_bill.html', context=patientD)


def pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return


def download_pdf_view(request, pk):
    discharge = models.Discharge.objects.all().filter(patient_id=pk).order_by('-id')[:1]
    dict = {
        'patientName': discharge[0].patientName,
        'assignedTherapistName': discharge[0].assignedTherapistName,
        'address': discharge[0].address,
        'phone_number': discharge[0].phone_number,
        'symptoms': discharge[0].symptoms,
        'registerDate': discharge[0].registerDate,
        'lastVisitDate': discharge[0].lastVisitDate,
        'visitNumber': discharge[0].visitNumber,
        'treatmentCost': discharge[0].treatmentCost,
        'copay': discharge[0].copay,
        'therapistFee': discharge[0].therapistFee,
        'otherCharge': discharge[0].otherCharge,
        'total': discharge[0].total,
    }
    return pdf('therapy/pdf_bill.html', dict)


@login_required(login_url='adminlogin')
@user_passes_test(admin_verified)
def admin_appointment_view(request):
    return render(request, 'therapy/admin_appointment.html')


@login_required(login_url='adminlogin')
@user_passes_test(admin_verified)
def admin_appointment_record_view(request):
    appointments = models.Appointment.objects.all().filter(status=True)
    return render(request, 'therapy/admin_appointment_record.html', {'appointments': appointments})


@login_required(login_url='adminlogin')
@user_passes_test(admin_verified)
def delete_admin_appointment_view(request, pk):
    appointment = models.Appointment.objects.get(id=pk)
    appointment.delete()
    return redirect('admin-appointment-record')


@login_required(login_url='adminlogin')
@user_passes_test(admin_verified)
def update_admin_appointment_view(request, pk):
    appointment = models.Appointment.objects.get(id=pk)
    appointmentForm = forms.AppointmentForm(request.FILES, instance=appointment)
    mydict = {'appointmentForm': appointmentForm, 'appointment': appointment}
    if request.method == 'POST':
        appointmentForm = forms.AppointmentForm(request.POST, request.FILES, instance=appointment)
        if appointmentForm.is_valid():
            appointment = appointmentForm.save(commit=False)
            appointment.therapist_id = request.POST.get('therapist_id')
            appointment.patient_id = request.POST.get('patient_id')
            appointment.therapistName = models.User.objects.get(id=request.POST.get('therapist_id')).first_name \
                                        + " " + models.User.objects.get(id=request.POST.get('therapist_id')).last_name
            appointment.patientName = models.User.objects.get(id=request.POST.get('patient_id')).first_name \
                                      + " " + models.User.objects.get(id=request.POST.get('patient_id')).last_name
            appointment.appointmentDate = request.POST.get('appointmentDate')
            appointment.status = True
            appointment.save()
            return redirect('admin-appointment-record')
    return render(request, 'therapy/admin_update_appointment.html', context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(admin_verified)
def admin_add_appointment_view(request):
    appointmentForm = forms.AppointmentForm()
    mydict = {'appointmentForm': appointmentForm, }
    if request.method == 'POST':
        appointmentForm = forms.AppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointment = appointmentForm.save(commit=False)
            appointment.therapist_id = request.POST.get('therapist_id')
            appointment.patient_id = request.POST.get('patient_id')
            appointment.therapistName = models.User.objects.get(id=request.POST.get('therapist_id')).first_name \
                                        + " " + models.User.objects.get(id=request.POST.get('therapist_id')).last_name
            appointment.patientName = models.User.objects.get(id=request.POST.get('patient_id')).first_name \
                                      + " " + models.User.objects.get(id=request.POST.get('patient_id')).last_name
            appointment.appointmentDate = request.POST.get('appointmentDate')
            appointment.status = True
            appointment.save()
        return HttpResponseRedirect('admin-appointment-record')
    return render(request, 'therapy/admin_add_appointment.html', context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(admin_verified)
def admin_approve_appointment_view(request):
    # those whose approval are needed
    appointments = models.Appointment.objects.all().filter(status=False)
    return render(request, 'therapy/admin_approve_appointment.html', {'appointments': appointments})


@login_required(login_url='adminlogin')
@user_passes_test(admin_verified)
def approve_appointment_view(request, pk):
    appointment = models.Appointment.objects.get(id=pk)
    appointment.status = True
    appointment.save()
    return redirect(reverse('admin-approve-appointment'))


@login_required(login_url='adminlogin')
@user_passes_test(admin_verified)
def reject_appointment_view(request, pk):
    appointment = models.Appointment.objects.get(id=pk)
    appointment.delete()
    return redirect('admin-approve-appointment')


@login_required(login_url='therapistlogin')
@user_passes_test(therapist_verified)
def therapist_page_view(request):
    appointment_count = models.Appointment.objects.all().filter(status=True, therapist_id=request.user.id).count()
    patient_discharge = models.Discharge.objects.all().distinct().filter(
        assignedTherapistName=request.user.first_name).count()
    appointments = models.Appointment.objects.all().filter(status=True, therapist_id=request.user.id).order_by('-id')
    patient_id = []
    for a in appointments:
        patient_id.append(a.patient_id)
    patients = models.Patient.objects.all().filter(status=True, user_id__in=patient_id).order_by('-id')
    patient_count = models.Patient.objects.all().filter(status=True, user_id__in=patient_id).count()
    mydict = {
        'patient_count': patient_count,
        'appointment_count': appointment_count,
        'patient_discharge': patient_discharge,
        'patients': patients,
        'appointments': appointments,
    }
    return render(request, 'therapy/therapist_page.html', context=mydict)


@login_required(login_url='therapistlogin')
@user_passes_test(therapist_verified)
def therapist_patient_view(request):
    return render(request, 'therapy/therapist_patient.html')


@login_required(login_url='therapistlogin')
@user_passes_test(therapist_verified)
def therapist_patient_record_view(request):
    appointments = models.Appointment.objects.all().filter(status=True, therapist_id=request.user.id)
    patient_id = []
    for a in appointments:
        patient_id.append(a.patient_id)
    patients = models.Patient.objects.all().filter(status=True, user_id__in=patient_id)
    appointments = zip(appointments, patients)
    return render(request, 'therapy/therapist_patient_record.html', {'appointments': appointments})


@login_required(login_url='therapistlogin')
@user_passes_test(therapist_verified)
def therapist_discharge_patient_view(request):
    discharge_patients = models.Discharge.objects.all().distinct().filter(
        assignedTherapistName=request.user.first_name + " " + request.user.last_name)
    return render(request, 'therapy/therapist_discharge_patient.html', {'discharge_patients': discharge_patients})


@login_required(login_url='therapistlogin')
@user_passes_test(therapist_verified)
def therapist_appointment_record_view(request):
    appointments = models.Appointment.objects.all().filter(status=True, therapist_id=request.user.id)
    patient_id = []
    for a in appointments:
        patient_id.append(a.patient_id)
    patients = models.Patient.objects.all().filter(status=True, user_id__in=patient_id)
    appointments = zip(appointments, patients)
    return render(request, 'therapy/therapist_appointment_record.html', {'appointments': appointments})


@login_required(login_url='therapistlogin')
@user_passes_test(therapist_verified)
def delete_appointment_view(request, pk):
    appointment = models.Appointment.objects.get(id=pk)
    appointment.delete()
    appointments = models.Appointment.objects.all().filter(status=True, therapist_id=request.user.id)
    patient_id = []
    for a in appointments:
        patient_id.append(a.patient_id)
    patients = models.Patient.objects.all().filter(status=True, user_id__in=patient_id)
    appointments = zip(appointments, patients)
    return render(request, 'therapy/therapist_delete_appointment.html',
                  {'appointments': appointments})


@login_required(login_url='patientlogin')
@user_passes_test(patient_verified)
def patient_page_view(request):
    patient = models.Patient.objects.get(user_id=request.user.id)
    therapist = models.Therapist.objects.get(user_id=patient.assignedTherapist)
    mydict = {
        'therapistName': therapist.get_name(),
        'therapistPhoneNumber': therapist.phone_number,
        'symptoms': patient.symptoms,
        'therapistDepartment': therapist.department,
        'registerDate': patient.registerDate,
        'address': patient.address,
    }
    return render(request, 'therapy/patient_page.html', context=mydict)


@login_required(login_url='patientlogin')
@user_passes_test(patient_verified)
def patient_appointment_view(request):
    patient = models.Patient.objects.get(user_id=request.user.id)
    return render(request, 'therapy/patient_appointment.html', {'patient': patient})


@login_required(login_url='patientlogin')
@user_passes_test(patient_verified)
def patient_book_appointment_view(request):
    appointmentForm = forms.PatientAppointmentForm()
    patient = models.Patient.objects.get(user_id=request.user.id)
    mydict = {'appointmentForm': appointmentForm, 'patient': patient}
    if request.method == 'POST':
        appointmentForm = forms.PatientAppointmentForm(request.POST)
        if appointmentForm.is_valid():
            print(request.POST.get('therapist_id'))
            therapist = models.Therapist.objects.get(user_id=request.POST.get('therapist_id'))
            appointment = appointmentForm.save(commit=False)
            appointment.therapist_id = request.POST.get('therapist_id')
            appointment.appointmentDate = request.POST.get('appointmentDate')
            appointment.patient_id = request.user.id
            appointment.therapistName = models.User.objects.get(id=request.POST.get('therapist_id')).first_name \
                                        + " " + models.User.objects.get(id=request.POST.get('therapist_id')).last_name
            appointment.patientName = request.user.first_name + " " + request.user.last_name
            appointment.status = False
            appointment.save()
        return HttpResponseRedirect('patient-appointment-record')
    return render(request, 'therapy/patient_book_appointment.html', context=mydict)


def patient_therapist_record_view(request):
    therapists = models.Therapist.objects.all().filter(status=True)
    return render(request, 'therapy/patient_therapist_record.html', {'patient': patient, 'therapists': therapists})


@login_required(login_url='patientlogin')
@user_passes_test(patient_verified)
def patient_appointment_record_view(request):
    appointments = models.Appointment.objects.all().filter(patient_id=request.user.id)
    return render(request, 'therapy/patient_appointment_record.html',
                  {'appointments': appointments, 'patient': patient})


@login_required(login_url='patientlogin')
@user_passes_test(patient_verified)
def patient_discharge_view(request):
    patient = models.Patient.objects.get(user_id=request.user.id)
    dischargeDetails = models.Discharge.objects.all().filter(patient_id=patient.id).order_by('-id')[:1]
    patientD = None
    if dischargeDetails:
        patientD = {
            'status': True,
            'patient': patient,
            'patient_id': patient.id,
            'patientName': patient.get_name(),
            'assignedTherapistName': dischargeDetails[0].assignedTherapistName,
            'address': patient.address,
            'phone_number': patient.phone_number,
            'symptoms': patient.symptoms,
            'registerDate': patient.registerDate,
            'lastVisitDate': dischargeDetails[0].lastVisitDate,
            'visitNumber': dischargeDetails[0].visitNumber,
            'treatmentCost': dischargeDetails[0].treatmentCost,
            'copay': dischargeDetails[0].copay,
            'therapistFee': dischargeDetails[0].therapistFee,
            'otherCharge': dischargeDetails[0].otherCharge,
            'total': dischargeDetails[0].total,
        }
        print(patientD)
    else:
        patientD = {
            'status': False,
            'patient': patient,
            'patient_id': request.user.id,
        }
    return render(request, 'therapy/patient_discharge.html', context=patientD)