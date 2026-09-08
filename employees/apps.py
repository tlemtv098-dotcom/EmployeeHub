from django.apps import AppConfig


class EmployeesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "employees"
    verbose_name = "จัดการพนักงาน"

    def ready(self):
        # สร้าง Group Member + สิทธิ์ดู/เพิ่มพนักงาน (กันพังตอน migrate)
        try:
            from django.contrib.auth.models import Group, Permission

            group, _ = Group.objects.get_or_create(name="Member")
            perms = Permission.objects.filter(
                codename__in=["view_employee", "add_employee"],
                content_type__app_label="employees",
            )
            if perms.exists():
                group.permissions.add(*perms)
        except Exception:
            pass
