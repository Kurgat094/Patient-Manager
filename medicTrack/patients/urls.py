from django.urls import path
from . import views

urlpatterns = [
    path("", views.login, name="login"),
    path("/register", views.register, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard,name="dashboard"),
    path("patient-list/" ,views.getpatients,name="getpatients"),
    path("patients/add/", views.patient_add, name="patient_add"),
     path("patients/<int:id>/", views.viewpatient, name="viewpatient"),
     path("patients/<int:patient_id>/vitals/add/",views.add_vitals,name="add_vitals"),
     path("patients/<int:patient_id>/assessment/add/",views.add_assessment,name="add_assessment"),
     path("patients/<int:patient_id>/visits/get/",views.get_patient_visits,name="get_patient_visits"),
     path("patients/visits/get/",views.get_patient_visits,name="get_patient_visits"),
]