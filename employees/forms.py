from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Employee

# ฟอร์มสมัครสมาชิก - เปิดให้ทุกคนสมัครเองได้
# ฟิลด์: ชื่อผู้ใช้, อีเมล, รหัสผ่าน + ยืนยันรหัสผ่าน
# ตรวจสอบ: อีเมลต้องไม่ซ้ำในระบบ
class SignupForm(UserCreationForm):
    # ช่องอีเมล - บังคับกรอก และต้องไม่ซ้ำ
    email = forms.EmailField(required=True, label="อีเมล", widget=forms.EmailInput(attrs={"placeholder": "email@example.com"}))

    class Meta:
        model = User
        fields = ("username", "email")
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "ชื่อผู้ใช้"}),
        }
        labels = {
            "username": "ชื่อผู้ใช้",
        }

    # ตรวจสอบอีเมลซ้ำ - ป้องกันสมัครซ้ำด้วยอีเมลเดิม
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("อีเมลนี้ถูกใช้งานแล้ว")
        return email

# ฟอร์มจัดการข้อมูลพนักงาน
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            "first_name", "last_name", "address", "gender", "birth_date",
            "department", "salary", "email", "phone", "status", "photo"
        ]
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "เช่น สมชาย"}),
            "last_name": forms.TextInput(attrs={"placeholder": "เช่น ใจดี"}),
            "address": forms.Textarea(attrs={"rows": 3, "placeholder": "บ้านเลขที่ ถนน ตำบล อำเภอ จังหวัด"}),
            "birth_date": forms.DateInput(attrs={"type": "date"}),
            "salary": forms.NumberInput(attrs={"min": "0", "step": "0.01", "placeholder": "0.00"}),
            "email": forms.EmailInput(attrs={"placeholder": "employee@example.com"}),
            "phone": forms.TextInput(attrs={"placeholder": "08xxxxxxxx"}),
        }