from django.db import models
from django.urls import reverse

class Employee(models.Model):
    GENDER_CHOICES = [
        ("M", "ชาย"),
        ("F", "หญิง"),
        ("O", "อื่น ๆ"),
    ]

    DEPARTMENT_CHOICES = [
        ("IT", "เทคโนโลยีสารสนเทศ"),
        ("HR", "ทรัพยากรบุคคล"),
        ("FIN", "การเงินและบัญชี"),
        ("MKT", "การตลาด"),
        ("OPS", "ปฏิบัติการ"),
        ("ADMIN", "ธุรการ"),
    ]

    STATUS_CHOICES = [
        ("active", "ทำงานอยู่"),
        ("leave", "ลางาน"),
        ("inactive", "พ้นสภาพ"),
    ]

    first_name = models.CharField("ชื่อ", max_length=100)
    last_name = models.CharField("นามสกุล", max_length=100)
    address = models.TextField("ที่อยู่", blank=True)
    gender = models.CharField("เพศ", max_length=1, choices=GENDER_CHOICES)
    birth_date = models.DateField("วันเกิด")
    department = models.CharField("แผนก", max_length=20, choices=DEPARTMENT_CHOICES)
    salary = models.DecimalField("เงินเดือน", max_digits=10, decimal_places=2)
    email = models.EmailField("อีเมล", blank=True)
    phone = models.CharField("เบอร์โทรศัพท์", max_length=20, blank=True)
    status = models.CharField("สถานะ", max_length=20, choices=STATUS_CHOICES, default="active")
    photo = models.ImageField("รูปภาพ", upload_to="employees/", blank=True, null=True)
    created_at = models.DateTimeField("สร้างเมื่อ", auto_now_add=True)
    updated_at = models.DateTimeField("แก้ไขเมื่อ", auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "พนักงาน"
        verbose_name_plural = "พนักงาน"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse("employee_detail", kwargs={"pk": self.pk})

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
