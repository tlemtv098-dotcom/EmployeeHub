from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EmployeeForm, ProfileForm, SignupForm
from .models import Employee

# เช็กแอดมิน: staff หรือ superuser เท่านั้น (เช่น admin/1234)
def _is_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

# วิวสมัครสมาชิก - เปิดให้ทุกคนสมัครเองได้ ไม่ต้องแอดมินอนุมัติ
# GET: แสดงฟอร์มสมัคร, POST: บันทึก user ใหม่ -> เด้งไปหน้า login
def signup(request):
    # ถ้าล็อกอินอยู่แล้ว ไม่ต้องสมัครซ้ำ -> ไป dashboard เลย
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        # รับข้อมูลจากฟอร์มสมัคร
        form = SignupForm(request.POST)
        if form.is_valid():
            # บันทึกผู้ใช้ใหม่ลงฐานข้อมูล
            user = form.save()
            # สมัครใหม่เข้า Group Member อัตโนมัติ (ดู/เพิ่มพนักงานได้)
            try:
                member_group, _ = Group.objects.get_or_create(name="Member")
                user.groups.add(member_group)
            except Exception:
                pass
            # แจ้งสำเร็จ -> ให้ไปล็อกอินเอง (ไม่ auto-login)
            messages.success(request, "สมัครสมาชิกสำเร็จ กรุณาเข้าสู่ระบบ")
            return redirect("login")
    else:
        # แสดงฟอร์มเปล่า
        form = SignupForm()
    return render(request, "registration/signup.html", {"form": form})

# หน้าแดชบอร์ด - ต้องล็อกอินก่อน
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

# หน้ารายชื่อพนักงาน - ค้นหา/กรอง/แบ่งหน้า
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

# เพิ่มพนักงานใหม่
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

# ดูรายละเอียดพนักงาน
@login_required
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, "employees/detail.html", {"employee": employee})

# แก้ไขข้อมูลพนักงาน - เฉพาะแอดมิน/staff (Member เจอ 403 ภาษาไทย)
@login_required
def employee_update(request, pk):
    if not _is_admin(request.user):
        return render(request, "403.html", status=403)
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

# ดูโปรไฟล์ตัวเอง - ต้องล็อกอินก่อน
@login_required
def profile(request):
    return render(request, "registration/profile.html")

# แก้ไขโปรไฟล์ตัวเอง - GET แสดงฟอร์ม, POST บันทึกแล้วเด้งไปหน้าโปรไฟล์
@login_required
def profile_edit(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "บันทึกข้อมูลโปรไฟล์เรียบร้อยแล้ว")
            return redirect("profile")
    else:
        form = ProfileForm(instance=request.user)
    return render(request, "registration/profile_edit.html", {"form": form})

# ลบพนักงาน - เฉพาะแอดมิน/staff (Member เจอ 403 ภาษาไทย)
@login_required
def employee_delete(request, pk):
    if not _is_admin(request.user):
        return render(request, "403.html", status=403)
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == "POST":
        name = employee.full_name
        employee.delete()
        messages.success(request, f"ลบข้อมูล {name} แล้ว")
        return redirect("employee_list")
    return render(request, "employees/delete.html", {"employee": employee})