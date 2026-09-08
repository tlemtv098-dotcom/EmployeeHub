# EmployeeHub — ระบบจัดการพนักงาน (Django)

ระบบ CRUD พนักงาน ภาษาไทย: เพิ่ม/ดู/แก้ไข/ลบ, ค้นหา, กรองแผนก/สถานะ, แบ่งหน้า, อัปรูป, Dashboard สรุปยอด

**Stack:** Django 6.0 + Gunicorn + WhiteNoise + PostgreSQL (prod) / SQLite (local) + Pillow

## ฟีเจอร์
- Dashboard: จำนวนพนักงานทั้งหมด/ทำงานอยู่/ลา, จำนวนแผนก, 5 คนล่าสุด
- รายชื่อพนักงาน: ค้นหา (ชื่อ/อีเมล/เบอร์), กรองแผนก/สถานะ, แบ่งหน้า 8/หน้า
- จัดการพนักงาน: ฟอร์มครบ (ชื่อ, ที่อยู่, เพศ, วันเกิด, แผนก, เงินเดือน, อีเมล, เบอร์, สถานะ, รูป)
- Auth: `login_required` ทั้งระบบ, Login/Logout, สร้างแอดมิน `admin/1234` อัตโนมัติตอน deploy

## โครงสร้าง
```
config/ (settings, urls, wsgi)
employees/ (models, views, forms, urls, admin)
templates/ (base, employees/*, registration/login)
static/css/app.css
manage.py, requirements.txt, build.sh, render.yaml
```

## ติดตั้งบนเครื่อง (Windows / VS Code)

```powershell
py -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
# สร้างแอดมินเอง หรือใช้สคริปต์ build.sh จะสร้าง admin/1234 ให้
python manage.py createsuperuser
python manage.py runserver
```

เปิด http://127.0.0.1:8000/ -> Login ด้วยแอดมินที่สร้าง

> ทดสอบเร็ว: `python manage.py shell -c "from employees.models import Employee; print(Employee.objects.count())"`

## Deploy ขึ้น Render — แบบ Manual Web Service (ไม่ต้องใช้บัตร)

> Blueprint ต้องใช้บัตรเครดิต -> ใช้วิธี Manual นี้แทน

### 1) สร้าง PostgreSQL
Dashboard -> **New+ -> PostgreSQL** -> Name `employee-hub-db` | Region `Singapore` | Plan **Free** -> Create -> ก็อป **Internal Database URL**

### 2) สร้าง Web Service
**New+ -> Web Service** -> Connect `tlemtv098-dotcom/EmployeeHub` branch `main`

| ช่อง | ค่า |
|-----|-----|
| Name | `employee-hub-kpru` |
| Runtime | `Python 3` |
| Build Command | `./build.sh` |
| Start Command | `gunicorn config.wsgi:application` |
| Plan | `Free` |

**Environment Variables:**
- `PYTHON_VERSION` = `3.12.8`
- `SECRET_KEY` = Generate
- `DEBUG` = `False`
- `DATABASE_URL` = วาง Internal URL จากข้อ 1 (หรือ Add -> Database -> เลือก `employee-hub-db`)

กด **Create Web Service** -> ดู **Logs** ต้องเห็น:
```
131 static files copied
Applying employees.0001_initial... OK
admin password reset to 1234
```

### 3) ใช้งาน
URL เช่น `https://employee-hub-kpru.onrender.com` -> Login `admin` / `1234`
- เพิ่ม/แก้ไข/ลบ/ค้นหา/กรอง/แบ่งหน้า/อัปรูป
- หมายเหตุ: รูปใน `media/` หายเมื่อ redeploy (disk ชั่วคราว) -> ถ้าต้องเก็บถาวรให้ย้ายไป S3/Cloudinary

**คู่มือละเอียด:** ดู `docs/DEPLOY_RENDER.md`

**รายงานโครงสร้างระบบ (Word ภาษาไทย 8–10 หน้า):** ดู `docs/EmployeeHub_รายงานโครงสร้างระบบ.docx` (สำเนาเดียวกับไฟล์บน Desktop)

## Deploy แบบ Blueprint (ต้องมีบัตร)
New+ -> **Blueprint** -> เลือก repo -> Render อ่าน `render.yaml` สร้าง web+db ให้อัตโนมัติ -> Apply

## Build Script
`build.sh` ทำ: `pip install` -> `collectstatic --no-input` -> `migrate` -> สร้าง/รีเซ็ตรหัส `admin/1234` แบบ idempotent (ไม่ลบ user ทุกครั้ง)

## Environment
| ตัวแปร | local | Render |
|--------|-------|--------|
| `DEBUG` | `True` (default) | `False` |
| `SECRET_KEY` | `django-insecure-...` | Generate |
| `DATABASE_URL` | ไม่ตั้ง -> SQLite | `postgres://...` จาก DB |
| `RENDER_EXTERNAL_HOSTNAME` | ไม่มี | Render ใส่ให้ -> `ALLOWED_HOSTS` + `CSRF_TRUSTED_ORIGINS` อัตโนมัติ |

## License
ภายใน KPRU / ใช้ทดสอบ
