# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
        ('nurse', 'Nurse'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    specialization = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    qualification = models.CharField(max_length=100)
    experience_years = models.PositiveIntegerField()

    def __str__(self):
        return f"Dr. {self.user.get_full_name()}"

class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    contact = models.CharField(max_length=15)
    address = models.TextField()
    blood_group = models.CharField(max_length=5)
    medical_history = models.TextField(blank=True)

    def __str__(self):
        return self.user.get_full_name()

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    time_slot = models.CharField(max_length=20)
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='scheduled')

    def __str__(self):
        return f"{self.patient.user.get_full_name()} with Dr. {self.doctor.user.last_name} on {self.appointment_date}"
    
class LabTest(models.Model):
    TEST_STATUS = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    doctor = models.ForeignKey('Doctor', on_delete=models.SET_NULL, null=True)
    test_name = models.CharField(max_length=100)
    test_date = models.DateField(auto_now_add=True)
    result = models.TextField(blank=True, null=True)
    report_file = models.FileField(upload_to='lab_reports/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=TEST_STATUS, default='pending')

    def __str__(self):
        return f"{self.test_name} for {self.patient.user.get_full_name()}"
    
class Medicine(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    manufacturer = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    expiry_date = models.DateField()
    stock = models.PositiveIntegerField()

    def __str__(self):
        return self.name
    
class MedicineSale(models.Model):
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    sale_date = models.DateTimeField(auto_now_add=True)

    def get_total_price(self):
        return self.quantity * self.medicine.price

    def __str__(self):
        return f"{self.quantity} x {self.medicine.name} to {self.patient.user.get_full_name()}"

    
class InventoryItem(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)  # e.g. Equipment, Disposable
    quantity = models.PositiveIntegerField()
    unit = models.CharField(max_length=20, default='pcs')  # kg, pcs, boxes, etc.
    added_date = models.DateField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    expiry_date = models.DateField(blank=True, null=True)  # if applicable

    def __str__(self):
        return f"{self.name} ({self.quantity} {self.unit})"
    
class SecurityStaff(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE)
    shift_start = models.TimeField()
    shift_end = models.TimeField()
    phone = models.CharField(max_length=15)
    assigned_gate = models.CharField(max_length=50)

    def __str__(self):
        return f"Security: {self.user.get_full_name()}"

class EntryLog(models.Model):
    person_name = models.CharField(max_length=100)
    purpose = models.CharField(max_length=100)
    time_in = models.DateTimeField(auto_now_add=True)
    time_out = models.DateTimeField(blank=True, null=True)
    handled_by = models.ForeignKey(SecurityStaff, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.person_name} - {self.purpose} ({self.time_in})"



class Billing(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('esewa', 'eSewa'),
        ('fonepay', 'Fonepay'),
    ]

    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    appointment = models.ForeignKey('Appointment', on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0)

    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    payment_status = models.CharField(max_length=10, choices=[('paid', 'Paid'), ('pending', 'Pending')], default='pending')
    payment_date = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        self.total = self.amount + self.tax - self.discount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Bill #{self.id} - {self.patient.user.get_full_name()} - Rs. {self.total}"
  