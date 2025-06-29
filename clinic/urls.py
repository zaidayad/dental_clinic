from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_patient, name='register_patient'),
    path('edit/<int:patient_id>/', views.edit_patient, name='edit_patient'),  # صفحة تعديل المريض
    path('delete/<int:patient_id>/', views.delete_patient, name='delete_patient'),  # صفحة حذف المريض
    path('patient/<int:patient_id>/', views.patient_detail, name='patient_detail'),
    path('patient/<int:patient_id>/add_treatment/', views.add_treatment, name='add_treatment'),
    path('treatment/edit/<int:treatment_id>/', views.edit_treatment, name='edit_treatment'),
    path('treatment/delete/<int:treatment_id>/',views. delete_treatment, name='delete_treatment'),
    path('filter/', views.filter_treatments, name='filter_treatments'),
    path('export_treatments/', views.export_treatments_excel, name='export_treatments'),
    
]