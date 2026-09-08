from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Employee

# ฟอร์มสมัครสมาชิก - ภาษาไทยทั้งหมด เข้าใจง่าย
# ฟิลด์: ชื่อผู้ใช้, อีเมล, รหัสผ่าน + ยืนยันรหัสผ่าน
# ตรวจสอบ: อีเมลต้องไม่ซ้ำในระบบ
class SignupForm(UserCreationForm):
    # ช่องอีเมล - บังคับกรอก และต้องไม่ซ้ำ
    email = forms.EmailField(
        required=True,
        label="อีเมล",
        help_text="กรอกอีเมลที่ใช้งานได้จริง เช่น name@example.com",
        widget=forms.EmailInput(attrs={"placeholder": "อีเมลของคุณ"}),
        error_messages={"required": "กรุณากรอกอีเมล", "invalid": "รูปแบบอีเมลไม่ถูกต้อง"}
    )

    class Meta:
        model = User
        fields = ("username", "email")
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "ชื่อผู้ใช้ ภาษาอังกฤษ ไม่มีช่องว่าง"}),
        }
        labels = {
            "username": "ชื่อผู้ใช้",
        }
        help_texts = {
            "username": "ไม่เกิน 150 ตัวอักษร ใช้ได้เฉพาะ ตัวอักษร ตัวเลข และ @/./+/-/_",
        }
        error_messages = {
            "username": {
                "required": "กรุณากรอกชื่อผู้ใช้",
                "unique": "ชื่อผู้ใช้นี้ถูกใช้งานแล้ว",
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # แปลป้ายและคำอธิบายรหัสผ่านเป็นไทยทั้งหมด
        self.fields["password1"].label = "รหัสผ่าน"
        self.fields["password1"].help_text = "อย่างน้อย 8 ตัวอักษร ควรมีทั้งตัวอักษรและตัวเลข"
        self.fields["password1"].widget.attrs.update({"placeholder": "รหัสผ่านอย่างน้อย 8 ตัว"})
        self.fields["password2"].label = "ยืนยันรหัสผ่าน"
        self.fields["password2"].help_text = "กรอกรหัสผ่านซ้ำอีกครั้งให้ตรงกัน"
        self.fields["password2"].widget.attrs.update({"placeholder": "ยืนยันรหัสผ่าน"})
        # ข้อความ error ภาษาไทย
        self.fields["password1"].error_messages["required"] = "กรุณากรอกรหัสผ่าน"
        self.fields["password2"].error_messages["required"] = "กรุณายืนยันรหัสผ่าน"
        self.error_messages["password_mismatch"] = "รหัสผ่านทั้งสองช่องไม่ตรงกัน"

    # ตรวจสอบอีเมลซ้ำ - ป้องกันสมัครซ้ำด้วยอีเมลเดิม
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("อีเมลนี้ถูกใช้งานแล้ว กรุณาใช้อีเมลอื่น")
        return email

# ฟอร์มดู/แก้ไขโปรไฟล์ตัวเอง - ภาษาไทยทั้งหมด
# ฟิลด์: ชื่อผู้ใช้, อีเมล, ชื่อจริง, นามสกุล
# ตรวจสอบ: อีเมลต้องไม่ซ้ำ ยกเว้นอีเมลของตัวเอง
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "ชื่อผู้ใช้ ภาษาอังกฤษ ไม่มีช่องว่าง"}),
            "email": forms.EmailInput(attrs={"placeholder": "อีเมลของคุณ"}),
            "first_name": forms.TextInput(attrs={"placeholder": "เช่น สมชาย"}),
            "last_name": forms.TextInput(attrs={"placeholder": "เช่น ใจดี"}),
        }
        labels = {
            "username": "ชื่อผู้ใช้",
            "email": "อีเมล",
            "first_name": "ชื่อจริง",
            "last_name": "นามสกุล",
        }
        help_texts = {
            "username": "ไม่เกิน 150 ตัวอักษร ใช้ได้เฉพาะ ตัวอักษร ตัวเลข และ @/./+/-/_",
            "email": "กรอกอีเมลที่ใช้งานได้จริง เช่น name@example.com",
            "first_name": "ชื่อจริงของคุณ (ไม่บังคับ)",
            "last_name": "นามสกุลของคุณ (ไม่บังคับ)",
        }
        error_messages = {
            "username": {
                "required": "กรุณากรอกชื่อผู้ใช้",
                "unique": "ชื่อผู้ใช้นี้ถูกใช้งานแล้ว",
            },
            "email": {
                "required": "กรุณากรอกอีเมล",
                "invalid": "รูปแบบอีเมลไม่ถูกต้อง",
            },
        }

    # ตรวจสอบอีเมลซ้ำ - ยกเว้นอีเมลของตัวเอง
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("อีเมลนี้ถูกใช้งานแล้ว กรุณาใช้อีเมลอื่น")
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