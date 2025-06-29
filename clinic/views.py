from django.shortcuts import render, redirect, get_object_or_404
from .models import Patient, Treatment

from .forms import PatientForm,TreatmentForm
from datetime import date  # استيراد تاريخ اليوم
from django.db.models import Sum
import os
import shutil
import openpyxl
from django.conf import settings
from openpyxl import Workbook
from django.http import HttpResponse
from openpyxl.drawing.image import Image as ExcelImage

def home(request):
    query = request.GET.get('q', '')  # الحصول على قيمة البحث من URL
    if query:
        patients = Patient.objects.filter(name__icontains=query)  # البحث عن المرضى الذين يحتوي اسمهم على النص المدخل
    else:
        patients = Patient.objects.all()  # إذا لم يتم إدخال نص البحث، عرض جميع المرضى

    return render(request, 'clinic/home.html', {'patients': patients, 'query': query})


def register_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            print(form.errors)
            form.save()
            return redirect('home')  # التأكد من أن إعادة التوجيه تتم بشكل صحيح إلى الصفحة الرئيسية
    else:
        form = PatientForm()

    return render(request, 'clinic/register_patient.html', {'form': form})

def edit_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PatientForm(instance=patient)
    
    return render(request, 'clinic/edit_patient.html', {'form': form, 'patient': patient})

# حذف مريض
def delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        patient.delete()
        return redirect('home')
    return render(request, 'clinic/confirm_delete.html', {'patient': patient})
def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    treatments = patient.treatments.all().order_by("-treatment_date")
    
    # إنشاء مجموعة من أرقام الأسنان المعالجة
    treated_teeth = set(treatment.tooth_number for treatment in treatments)
    
    # تعريف جميع الأسنان
    all_teeth = [
        'UR8', 'UR7', 'UR6', 'UR5', 'UR4', 'UR3', 'UR2', 'UR1',
        'UL1', 'UL2', 'UL3', 'UL4', 'UL5', 'UL6', 'UL7', 'UL8',
        'LR8', 'LR7', 'LR6', 'LR5', 'LR4', 'LR3', 'LR2', 'LR1',
        'LL1', 'LL2', 'LL3', 'LL4', 'LL5', 'LL6', 'LL7', 'LL8'
    ]
    
    return render(request, 'clinic/patient_detail.html', {
        'patient': patient,
        'treatments': treatments,
        'treated_teeth': treated_teeth,
        'all_teeth': all_teeth
    })

def add_treatment(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    
    # ترتيب الأسنان حسب الموقع التشريحي (من المركز إلى الخلف)
    upper_right_teeth = [
        ('UR1', 'الثنية المركزية العلوية اليمنى', '1'),
        ('UR2', 'الثنية الجانبية العلوية اليمنى', '2'),
        ('UR3', 'الناب العلوي الأيمن', '3'),
        ('UR4', 'الضوحك الأول العلوي الأيمن', '4'),
        ('UR5', 'الضوحك الثاني العلوي الأيمن', '5'),
        ('UR6', 'الضرس الأول العلوي الأيمن', '6'),
        ('UR7', 'الضرس الثاني العلوي الأيمن', '7'),
        ('UR8', 'ضرس العقل العلوي الأيمن', '8')
    ]
    
    upper_left_teeth = [
        ('UL1', 'الثنية المركزية العلوية اليسرى', '1'),
        ('UL2', 'الثنية الجانبية العلوية اليسرى', '2'),
        ('UL3', 'الناب العلوي الأيسر', '3'),
        ('UL4', 'الضوحك الأول العلوي الأيسر', '4'),
        ('UL5', 'الضوحك الثاني العلوي الأيسر', '5'),
        ('UL6', 'الضرس الأول العلوي الأيسر', '6'),
        ('UL7', 'الضرس الثاني العلوي الأيسر', '7'),
        ('UL8', 'ضرس العقل العلوي الأيسر', '8')
    ]
    
    lower_right_teeth = [
        ('LR1', 'الثنية المركزية السفلية اليمنى', '1'),
        ('LR2', 'الثنية الجانبية السفلية اليمنى', '2'),
        ('LR3', 'الناب السفلي الأيمن', '3'),
        ('LR4', 'الضوحك الأول السفلي الأيمن', '4'),
        ('LR5', 'الضوحك الثاني السفلي الأيمن', '5'),
        ('LR6', 'الضرس الأول السفلي الأيمن', '6'),
        ('LR7', 'الضرس الثاني السفلي الأيمن', '7'),
        ('LR8', 'ضرس العقل السفلي الأيمن', '8')
    ]
    
    lower_left_teeth = [
        ('LL1', 'الثنية المركزية السفلية اليسرى', '1'),
        ('LL2', 'الثنية الجانبية السفلية اليسرى', '2'),
        ('LL3', 'الناب السفلي الأيسر', '3'),
        ('LL4', 'الضوحك الأول السفلي الأيسر', '4'),
        ('LL5', 'الضوحك الثاني السفلي الأيسر', '5'),
        ('LL6', 'الضرس الأول السفلي الأيسر', '6'),
        ('LL7', 'الضرس الثاني السفلي الأيسر', '7'),
        ('LL8', 'ضرس العقل السفلي الأيسر', '8')
    ]

    if request.method == 'POST':
        form = TreatmentForm(request.POST, request.FILES)
        if form.is_valid():
            treatment = form.save(commit=False)
            treatment.patient = patient
            treatment.save()
            return redirect('patient_detail', patient_id=patient.id)
    else:
        form = TreatmentForm(initial={'treatment_date': date.today()})

    return render(request, 'clinic/add_treatment.html', {
        'form': form,
        'patient': patient,
        'upper_right_teeth': upper_right_teeth,
        'upper_left_teeth': upper_left_teeth,
        'lower_right_teeth': lower_right_teeth,
        'lower_left_teeth': lower_left_teeth,
    })
def edit_treatment(request, treatment_id):
    treatment = get_object_or_404(Treatment, id=treatment_id)
    
    if request.method == 'POST':
        form = TreatmentForm(request.POST, request.FILES, instance=treatment)  # <-- أضف request.FILES
        if form.is_valid():
            form.save()
            return redirect('patient_detail', patient_id=treatment.patient.id)
    else:
        form = TreatmentForm(instance=treatment)

    return render(request, 'clinic/edit_treatment.html', {'form': form, 'treatment': treatment})

def delete_treatment(request, treatment_id):
    treatment = get_object_or_404(Treatment, id=treatment_id)
    patient_id = treatment.patient.id  # نحفظ ID المريض قبل الحذف
    treatment.delete()
    return redirect('patient_detail', patient_id=patient_id)

def filter_treatments(request):
    treatments = Treatment.objects.all()
    
    # الحصول على تاريخ اليوم
    today = date.today().strftime('%Y-%m-%d')
    
    # جلب القيم من GET وإعطاء تاريخ اليوم كقيمة افتراضية
    start_date = request.GET.get('start_date', today)
    end_date = request.GET.get('end_date', today)
    treatment_type = request.GET.get('treatment_type')

    if treatment_type:
        treatments = treatments.filter(treatment_type=treatment_type)

    if start_date:
        treatments = treatments.filter(treatment_date__gte=start_date)

    if end_date:
        treatments = treatments.filter(treatment_date__lte=end_date)

    # حساب المجموع الكلي للمدفوعات بعد الفلترة
    total_amount = treatments.aggregate(total=Sum('amount_paid'))['total'] or 0

    return render(request, 'clinic/filter_treatments.html', {
        'treatments': treatments,
        'total_amount': total_amount,
        'start_date': start_date,
        'end_date': end_date,
    })

def export_treatments_excel(request):
    # إنشاء ملف Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "العلاجات"

    # رأس الجدول
    ws.append([
        'اسم المريض',
        'العمر',
        'رقم الهاتف',
        'تاريخ العلاج',
        'نوع العلاج',
        'رقم السن',
        'المبلغ الكلي',
        'المبلغ المدفوع',
        'المبلغ المتبقي',
        'رابط الصورة',
        'ملاحظات'
    ])

    # المسار الذي نريد نسخ الصور إليه
    backup_dir = os.path.join(settings.MEDIA_ROOT, 'backups')
    os.makedirs(backup_dir, exist_ok=True)

    treatments = Treatment.objects.select_related('patient').all()

    for treatment in treatments:
        image_url = ''
        if treatment.image:
            # رابط مباشر للصورة
            image_url = request.build_absolute_uri(treatment.image.url)

            # تجهيز اسم المريض وامتداد الصورة
            patient_name = treatment.patient.name.replace(" ", "_")
            ext = os.path.splitext(treatment.image.name)[1]
            new_image_name = f"{patient_name}_{treatment.id}{ext}"
            new_image_path = os.path.join(backup_dir, new_image_name)

            # نسخ الصورة إلى مجلد النسخ الاحتياطي
            try:
                shutil.copy(treatment.image.path, new_image_path)
            except Exception as e:
                print(f"❌ خطأ في نسخ صورة: {e}")

        # إضافة صف جديد
        ws.append([
            treatment.patient.name,
            treatment.patient.age,
            treatment.patient.phone,
            treatment.treatment_date.strftime('%Y-%m-%d'),
            treatment.get_treatment_type_display(),
            treatment.get_tooth_number_display(),
            treatment.first_installment,
            treatment.amount_paid,
            treatment.remaining_amount,
            image_url,
            treatment.note or ''
        ])

    # تجهيز الاستجابة
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=treatments_backup.xlsx'
    wb.save(response)

    return response