from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EmployeeForm
from .models import Employee

@login_required
def dashboard(request):
    employees = Employee.objects.all()
    context = {
        "total_employees": employees.count(),
        "active_employees": employees.filter(status="active").count(),
        "leave_employees": employees.filter(status="leave").count(),
        "departments": employees.values("department").distinct().count(),
        "recent_employees": employees[:5],
    }
    return render(request, "employees/dashboard.html", context)

@login_required
def employee_list(request):
    query = request.GET.get("q", "").strip()
    department = request.GET.get("department", "")
    status = request.GET.get("status", "")

    employees = Employee.objects.all()

    if query:
        employees = employees.filter(
            Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(email__icontains=query)
            | Q(phone__icontains=query)
        )

    if department:
        employees = employees.filter(department=department)

    if status:
        employees = employees.filter(status=status)

    paginator = Paginator(employees, 8)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "employees/list.html", {
        "page_obj": page_obj,
        "query": query,
        "selected_department": department,
        "selected_status": status,
        "department_choices": Employee.DEPARTMENT_CHOICES,
        "status_choices": Employee.STATUS_CHOICES,
    })

@login_required
def employee_create(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            employee = form.save()
            messages.success(request, f"เพิ่มข้อมูล {employee.full_name} เรียบร้อยแล้ว")
            return redirect("employee_detail", pk=employee.pk)
    else:
        form = EmployeeForm()
    return render(request, "employees/form.html", {"form": form, "title": "เพิ่มพนักงานใหม่", "button_text": "บันทึกข้อมูล"})

@login_required
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, "employees/detail.html", {"employee": employee})

@login_required
def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == "POST":
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            employee = form.save()
            messages.success(request, "แก้ไขข้อมูลพนักงานเรียบร้อยแล้ว")
            return redirect("employee_detail", pk=employee.pk)
    else:
        form = EmployeeForm(instance=employee)
    return render(request, "employees/form.html", {"form": form, "title": "แก้ไขข้อมูลพนักงาน", "button_text": "บันทึกการแก้ไข", "employee": employee})

@login_required
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == "POST":
        name = employee.full_name
        employee.delete()
        messages.success(request, f"ลบข้อมูล {name} แล้ว")
        return redirect("employee_list")
    return render(request, "employees/delete.html", {"employee": employee})
