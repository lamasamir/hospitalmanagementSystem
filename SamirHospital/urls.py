from django.urls import path
from . import views
 

urlpatterns = [
     path('', views.login_dashboard, name='login_dashboard'),
    # AUTH & DASHBOARD
    path('register/', views.register_user, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
   
    #Login and Logout
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # Admin specific views
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('create-admin/', views.create_admin_user, name='create_admin'),

    # DEPARTMENT
    path('departments/', views.department_list, name='department_list'),
    path('departments/add/', views.department_create, name='department_create'),

    # DOCTOR
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctors/add/', views.doctor_create, name='doctor_create'),
    
    # PATIENT
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/add/', views.patient_create, name='patient_create'),

    # APPOINTMENT
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/book/', views.appointment_create, name='appointment_create'),

    # LAB TEST
    path('labtests/', views.labtest_list, name='labtest_list'),
    path('labtests/add/', views.labtest_create, name='labtest_create'),

    # MEDICINE
    path('medicines/', views.medicine_list, name='medicine_list'),
    path('medicines/add/', views.medicine_create, name='medicine_create'),

    # INVENTORY
    path('inventory/', views.inventory_list, name='inventory_list'),
    path('inventory/add/', views.inventory_create, name='inventory_create'),

    # SECURITY STAFF
    path('security/', views.security_list, name='security_list'),
    path('security/add/', views.security_create, name='security_create'),

    # ENTRY LOG
    path('entrylogs/', views.entrylog_list, name='entrylog_list'),
    path('entrylogs/add/', views.entrylog_create, name='entrylog_create'),

    # BILLING
    path('billing/', views.billing_list, name='billing_list'),
    path('billing/create/', views.billing_create, name='billing_create'),
]

