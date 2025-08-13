from django import forms
from .models import Patient
from .models import Treatment
from .models import Appointment
from datetime import date  
class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'age', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'أدخل اسم المريض'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'أدخل العمر'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'أدخل رقم الهاتف'}),
        }

class TreatmentForm(forms.ModelForm):
    class Meta:
        
        model = Treatment
        fields = ['treatment_type', 'tooth_number', 'amount_paid', 'treatment_date', 'image','note','first_installment','remaining_amount']
        widgets = {
            'treatment_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'treatment_type': forms.Select(attrs={'class': 'form-control'}),
            'tooth_number': forms.Select(attrs={'class': 'form-control'}),
            'amount_paid': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'المبلغ المدفوع'}),
            'note': forms.Textarea(attrs={'rows': 3, 'placeholder': 'أضف ملاحظة عن الحالة...'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ضبط القيمة الافتراضية لحقل التاريخ
        if not self.instance.pk:  # فقط عند الإضافة وليس التعديل
            self.fields['treatment_date'].initial = date.today()

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient_name', 'date', 'time', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }