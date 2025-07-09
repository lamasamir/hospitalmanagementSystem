from django import forms
from .models import (
    Appointment, LabTest, MedicineSale, Billing,
    InventoryItem, SecurityStaff, EntryLog,
    CustomUser, Doctor, Patient, Department , Medicine
)
from django.contrib.auth.forms import UserCreationForm


# ----------------------------
# User Registration Form
# ----------------------------
class CustomUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'password1', 'password2']

# ------------------------
# Department Form
# -------------------------

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description'] 


# ----------------------------
# Patient Form
# ----------------------------
class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['date_of_birth', 'gender', 'contact', 'address', 'blood_group', 'medical_history']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }


# ----------------------------
# Doctor Form
# ----------------------------
class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['department', 'specialization', 'phone', 'qualification', 'experience_years']


# ----------------------------
# Appointment Form
# ----------------------------
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'appointment_date', 'time_slot', 'reason', 'status']
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
        }


# ----------------------------
# Lab Test Form
# ----------------------------
class LabTestForm(forms.ModelForm):
    class Meta:
        model = LabTest
        fields = ['patient', 'doctor', 'test_name', 'result', 'report_file', 'status']
# ------------------------
# Medicine Form
# ------------------------

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = '__all__' 
# ----------------------------
# Medicine Sale Form
# ----------------------------
class MedicineSaleForm(forms.ModelForm):
    class Meta:
        model = MedicineSale
        fields = ['patient', 'medicine', 'quantity']


# ----------------------------
# Billing Form
# ----------------------------
class BillingForm(forms.ModelForm):
    class Meta:
        model = Billing
        fields = ['patient', 'appointment', 'amount', 'tax', 'discount', 'payment_method', 'payment_status', 'description']


# ----------------------------
# Inventory Item Form
# ----------------------------
class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ['name', 'category', 'quantity', 'unit', 'expiry_date']
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }


# ----------------------------
# Security Staff Form
# ----------------------------
class SecurityStaffForm(forms.ModelForm):
    class Meta:
        model = SecurityStaff
        fields = ['user', 'shift_start', 'shift_end', 'phone', 'assigned_gate']


# ----------------------------
# Entry Log Form
# ----------------------------
class EntryLogForm(forms.ModelForm):
    class Meta:
        model = EntryLog
        fields = ['person_name', 'purpose', 'time_out', 'handled_by']
        widgets = {
            'time_out': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
