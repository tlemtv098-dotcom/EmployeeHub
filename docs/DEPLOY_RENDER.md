# คู่มือ Deploy EmployeeHub ขึ้น Render

> มี 2 วิธี - Blueprint ต้องใช้บัตรเครดิต, **Manual Web Service ไม่ต้อง** (แนะนำตอนนี้)

## วิธี A: Manual Web Service (แนะนำ - ไม่ขอบัตร)

### 1. เช็คโค้ดบน GitHub
- https://github.com/tlemtv098-dotcom/EmployeeHub ต้องเห็น commit `ca7e454` ขึ้นไป

### 2. สร้าง PostgreSQL ก่อน
1. Dashboard -> New+ -> **PostgreSQL**
2. Name: `employee-hub-db` | Plan: **Free** | Create
3. รอ Status `Available` -> ก็อปปี้ **Internal Database URL** ไว้

### 3. สร้าง Web Service
1. New+ -> **Web Service** -> Connect repo `tlemtv098-dotcom/EmployeeHub` branch `main`
2. ตั้งค่า:
   - Name: `employee-hub-kpru` (หรือชื่ออะไรก็ได้)
   - Runtime: `Python 3`
   - Region: `Singapore` (ใกล้ไทย)
   - Build Command: `./build.sh`
   - Start Command: `gunicorn config.wsgi:application`
   - Plan: **Free**
3. **Environment Variables** กด Add:
   - `PYTHON_VERSION` = `3.12.8`
   - `SECRET_KEY` = กด Generate
   - `DEBUG` = `False`
   - `DATABASE_URL` = วาง Internal Database URL จากข้อ 2 (หรือกด Add -> Database -> employee-hub-db)
   - ไม่ต้องใส่ `ALLOWED_HOSTS` / `CSRF_TRUSTED_ORIGINS` เอง - `settings.py` อ่าน `RENDER_EXTERNAL_HOSTNAME` ให้แล้ว
4. กด **Create Web Service**

### 4. ดู Logs
ต้องเห็น:
```
pip install -r requirements.txt
131 static files copied
Applying employees.0001_initial OK
admin password reset to 1234 / created admin/1234
```
ถ้า `no such table` = `migrate` ยังไม่รัน -> เข้า Shell รัน `python manage.py migrate`

### 5. ทดสอบ
- URL: `https://employee-hub-kpru.onrender.com` (ดูบน Dashboard)
- Login `admin` / `1234`
- [ ] เพิ่มพนักงาน -> บันทึกได้ | [ ] แก้ไข/ลบ/ค้นหา | [ ] อัปรูป
- รูปใน `media/` จะหายเมื่อ redeploy (รับได้สำหรับทดสอบ)

---

## วิธี B: Blueprint (ต้องมีบัตรเครดิต)
1. New+ -> **Blueprint** -> Connect repo -> Render อ่าน `render.yaml` (web + db)
2. Apply -> รอสร้างคู่
> ถ้าขอบัตร -> ใช้วิธี A แทน `render.yaml` จะถูกข้ามไป

---

## แก้ปัญหา
- **500 ตอน login** -> เช็ค `CSRF` -> ต้อง push ล่าสุดที่มี `CSRF_TRUSTED_ORIGINS` แล้ว redeploy
- **Build fail** -> ดูบรรทัดแดงแรก, ลอง Clear cache & Deploy
- **DB ต่อไม่ติด** -> เช็ค `DATABASE_URL` ใน Web Service ว่าลิงก์กับ `employee-hub-db` แล้ว
- **อยากเปลี่ยนรหัส admin**: Render Shell -> `python manage.py shell`
```python
from django.contrib.auth import get_user_model
u=get_user_model().objects.get(username='admin'); u.set_password('รหัสใหม่'); u.save()
```

---
ล่าสุด: `build.sh` idempotent + `DEBUG=False` + `CSRF_TRUSTED_ORIGINS` | ทดสอบ local `py manage.py check` + `collectstatic` ผ่าน
