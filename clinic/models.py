from django.db import models
from datetime import date
import os

class Patient(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, unique=True)
    age = models.PositiveIntegerField(default=18)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

def patient_image_upload_path(instance, filename):
    """ حفظ الصور باسم المريض داخل مجلد 'treatments/' """
    ext = filename.split('.')[-1]  # استخراج امتداد الصورة
    filename = f"{instance.patient.name.replace(' ', '_')}.{ext}"  # حفظ باسم المريض
    return os.path.join('treatments/', filename)

class Treatment(models.Model):
    TOOTH_CHOICES = [
    # الفك العلوي (Maxillary)
    ('UR8', 'ضرس العقل العلوي الأيمن (UR8)'),
    ('UR7', 'الضرس الثاني العلوي الأيمن (UR7)'),
    ('UR6', 'الضرس الأول العلوي الأيمن (UR6)'),
    ('UR5', 'الناب الثاني العلوي الأيمن (UR5)'),
    ('UR4', 'الناب الأول العلوي الأيمن (UR4)'),
    ('UR3', 'الرباعية العلوية اليمنى (UR3)'),
    ('UR2', 'الثنية العلوية اليمنى (UR2)'),
    ('UR1', 'الثنية المركزية العلوية اليمنى (UR1)'),
    ('UL1', 'الثنية المركزية العلوية اليسرى (UL1)'),
    ('UL2', 'الثنية العلوية اليسرى (UL2)'),
    ('UL3', 'الرباعية العلوية اليسرى (UL3)'),
    ('UL4', 'الناب الأول العلوي الأيسر (UL4)'),
    ('UL5', 'الناب الثاني العلوي الأيسر (UL5)'),
    ('UL6', 'الضرس الأول العلوي الأيسر (UL6)'),
    ('UL7', 'الضرس الثاني العلوي الأيسر (UL7)'),
    ('UL8', 'ضرس العقل العلوي الأيسر (UL8)'),
    
    # الفك السفلي (Mandibular)
    ('LR8', 'ضرس العقل السفلي الأيمن (LR8)'),
    ('LR7', 'الضرس الثاني السفلي الأيمن (LR7)'),
    ('LR6', 'الضرس الأول السفلي الأيمن (LR6)'),
    ('LR5', 'الناب الثاني السفلي الأيمن (LR5)'),
    ('LR4', 'الناب الأول السفلي الأيمن (LR4)'),
    ('LR3', 'الرباعية السفلية اليمنى (LR3)'),
    ('LR2', 'الثنية السفلية اليمنى (LR2)'),
    ('LR1', 'الثنية المركزية السفلية اليمنى (LR1)'),
    ('LL1', 'الثنية المركزية السفلية اليسرى (LL1)'),
    ('LL2', 'الثنية السفلية اليسرى (LL2)'),
    ('LL3', 'الرباعية السفلية اليسرى (LL3)'),
    ('LL4', 'الناب الأول السفلي الأيسر (LL4)'),
    ('LL5', 'الناب الثاني السفلي الأيسر (LL5)'),
    ('LL6', 'الضرس الأول السفلي الأيسر (LL6)'),
    ('LL7', 'الضرس الثاني السفلي الأيسر (LL7)'),
    ('LL8', 'ضرس العقل السفلي الأيسر (LL8)'),
]
    TREATMENT_CHOICES = [
        ('حشوه موقتة', 'حشوة موقتة'),
        ('حشوه دائمه', 'حشوة دائمة'),
        ('قلع', 'قلع'),
        ('زراعة', 'زراعة'),
        ('جذر', 'جذر'),
        
    ]  # الخيارات المتاحة

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="treatments")
    treatment_date = models.DateField(default=date.today)
    treatment_type = models.CharField(max_length=20, choices=TREATMENT_CHOICES)  # حقل نوع الحالة
    tooth_number = models.CharField(max_length=3, choices=TOOTH_CHOICES)  # حقل رقم السن
    amount_paid = models.PositiveBigIntegerField(null=False, blank=True)
    first_installment = models.PositiveBigIntegerField( null=False, blank=True)
    image = models.ImageField(upload_to=patient_image_upload_path, blank=True, null=True)  # 🔥 إضافة الصورة
    note = models.TextField(blank=True, null=True)
    remaining_amount = models.PositiveBigIntegerField(default=0, null=False, blank=True)
  
    

    
    def save(self, *args, **kwargs):
        if self.first_installment is None:
            self.first_installment = 0
        if self.amount_paid is None:
            self.amount_paid = 0
        
        self.remaining_amount = max(self.amount_paid - self.first_installment, 0)
        super().save(*args, **kwargs)
    def __str__(self):
        return f"حالة {self.patient.name} - {self.get_treatment_type_display()} في {self.date}"

