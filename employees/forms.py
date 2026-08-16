from django import forms
from .models import Employee

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
