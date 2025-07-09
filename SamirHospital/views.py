from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login , logout
from django.http import HttpResponseForbidden
from django.contrib import messages
from .models import (
    Department, Doctor, Patient, Appointment, LabTest,
    Medicine, MedicineSale, InventoryItem, SecurityStaff,
    EntryLog, Billing
)
from .forms import (
    CustomUserForm, DepartmentForm, DoctorForm, PatientForm, 
    AppointmentForm, LabTestForm, MedicineForm, 
    MedicineSaleForm, InventoryItemForm, SecurityStaffForm, 
    EntryLogForm, BillingForm
)

def login_dashboard(request):
    # If already logged in, redirect based on role
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'hospital/logindashboard.html')



# ========== USER AUTHENTICATION & DASHBOARD ==========

def register_user(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            # Prevent selecting admin role during public registration
            if form.cleaned_data['role'] == 'admin':
                return HttpResponseForbidden("You cannot choose admin role.")
            
            user.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserForm()
    return render(request, 'hospital/register.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'hospital/dashboard.html')

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser and request.user.role != 'admin':
        return HttpResponseForbidden("Access denied.")

    context = {
        'total_patients': Patient.objects.count(),
        'total_doctors': Doctor.objects.count(),
        'total_appointments': Appointment.objects.count(),
        'total_labtests': LabTest.objects.count(),
        'total_medicines': Medicine.objects.count(),
        'total_inventory': InventoryItem.objects.count(),
        'total_bills': Billing.objects.count(),
    }
    return render(request, 'hospital/admin_dashboard.html', context)

@login_required
def create_admin_user(request):
    if not request.user.is_superuser and request.user.role != 'admin':
        return HttpResponseForbidden("Only admin or superuser can create another admin.")

    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'admin'  # Force role to admin
            user.save()
            return redirect('admin_dashboard')
    else:
        form = CustomUserForm()
    return render(request, 'hospital/forms.html', {'form': form, 'title': 'Create Admin User'})


# ========== DEPARTMENT ==========

@login_required
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'hospital/department_list.html', {'departments': departments})

@login_required
def department_create(request):
    if request.user.role != 'admin':
        return HttpResponseForbidden("Only admin can create departments.")
    form = DepartmentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('department_list')
    return render(request, 'hospital/forms.html', {'form': form, 'title': 'Add Department'})


# ========== DOCTOR ==========

@login_required
def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'hospital/doctor_list.html', {'doctors': doctors})

@login_required
def doctor_create(request):
    if request.user.role != 'admin':
        return HttpResponseForbidden("Only admin can add doctors.")
    form = DoctorForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('doctor_list')
    return render(request, 'hospital/forms.html', {'form': form, 'title': 'Add Doctor'})

# ========== PATIENT ==========

@login_required
def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'hospital/patients_list.html', {'patients': patients})

@login_required
def patient_create(request):
    if request.user.role != 'admin':
        return HttpResponseForbidden("Only admin can add patients.")
    form = PatientForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('patient_list')
    return render(request, 'hospital/forms.html', {'form': form, 'title': 'Add Patient'})


# ========== APPOINTMENT ==========

@login_required
def appointment_list(request):
    if request.user.role == 'doctor':
        appointments = Appointment.objects.filter(doctor__user=request.user)
    elif request.user.role == 'patient':
        appointments = Appointment.objects.filter(patient__user=request.user)
    else:
        appointments = Appointment.objects.all()
    return render(request, 'hospital/appointment_list.html', {'appointments': appointments})

@login_required
def appointment_create(request):
    # Only allow patients to book appointments
    if request.user.role != 'patient':
        return HttpResponseForbidden("Only patients can book appointments.")
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            # Auto-assign the logged-in patient
            appointment.patient = Patient.objects.get(user=request.user)
            appointment.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm()

    return render(request, 'hospital/forms.html', {'form': form, 'title': 'Book Appointment'})



# ========== LAB TEST ==========

@login_required
def labtest_list(request):
    labtests = LabTest.objects.all()
    return render(request, 'hospital/labtest_list.html', {'labtests': labtests})

@login_required
def labtest_create(request):
    form = LabTestForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('labtest_list')
    return render(request, 'hospital/forms.html', {'form': form, 'title': 'Add Lab Test'})


# ========== MEDICINE ==========

@login_required
def medicine_list(request):
    medicines = Medicine.objects.all()
    return render(request, 'hospital/medicine_list.html', {'medicines': medicines})

@login_required
def medicine_create(request):
    if request.user.role != 'admin':
        return HttpResponseForbidden("Only admin can add medicines.")
    form = MedicineForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('medicine_list')
    return render(request, 'hospital/forms.html', {'form': form, 'title': 'Add Medicine'})


# ========== INVENTORY ==========

@login_required
def inventory_list(request):
    items = InventoryItem.objects.all()
    return render(request, 'hospital/inventory_list.html', {'items': items})

@login_required
def inventory_create(request):
    if request.user.role != 'admin':
        return HttpResponseForbidden("Only admin can add inventory.")
    form = InventoryItemForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('inventory_list')
    return render(request, 'hospital/forms.html', {'form': form, 'title': 'Add Inventory Item'})


# ========== SECURITY ==========

@login_required
def security_list(request):
    staff = SecurityStaff.objects.all()
    return render(request, 'hospital/security_list.html', {'staff': staff})

@login_required
def security_create(request):
    if request.user.role != 'admin':
        return HttpResponseForbidden("Only admin can add security staff.")
    form = SecurityStaffForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('security_list')
    return render(request, 'hospital/forms.html', {'form': form, 'title': 'Add Security Staff'})


# ========== ENTRY LOG ==========

@login_required
def entrylog_list(request):
    logs = EntryLog.objects.all()
    return render(request, 'hospital/entrylog_list.html', {'logs': logs})

@login_required
def entrylog_create(request):
    if request.user.role != 'admin':
        return HttpResponseForbidden("Only admin can add entry logs.")
    form = EntryLogForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('entrylog_list')
    return render(request, 'hospital/forms.html', {'form': form, 'title': 'Add Entry Log'})


# ========== BILLING ==========

@login_required
def billing_list(request):
    billings = Billing.objects.all()
    return render(request, 'hospital/billing_list.html', {'billings': billings})

@login_required
def billing_create(request):
    if request.user.role != 'admin':
        return HttpResponseForbidden("Only admin can create bills.")
    form = BillingForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('billing_list')
    return render(request, 'hospital/forms.html', {'form': form, 'title': 'Create Bill'})
# Login view
def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  # ✅ Make sure 'dashboard' URL name exists
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'hospital/login.html', {'form': form})
#Logout view
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('login')