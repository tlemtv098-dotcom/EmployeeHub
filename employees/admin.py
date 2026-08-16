from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "department", "salary", "status", "created_at")
    list_filter = ("department", "gender", "status")
    search_fields = ("first_name", "last_name", "email", "phone")
    ordering = ("-created_at",)
