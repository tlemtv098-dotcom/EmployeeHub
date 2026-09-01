# คู่มือ Deploy EmployeeHub ขึ้น Render (Blueprint)

> ทำตามทีละขั้น กดตามได้เลย - ใช้ `render.yaml` ที่มีใน repo

## 1. เช็คโค้ดบน GitHub
- เปิด https://github.com/tlemtv098-dotcom/EmployeeHub
- ต้องเห็น commit ล่าสุด `Render hardening: idempotent build.sh...` (00dd7cc)
- ถ้ายังไม่เห็น = push ไม่สำเร็จ ให้รัน `git push origin main` อีกรอบ

## 2. สร้าง Blueprint บน Render
1. เข้า https://dashboard.render.com -> **New +** -> **Blueprint**
2. Connect repo `tlemtv098-dotcom/EmployeeHub` (ถ้ายังไม่ connect ให้ Authorize GitHub)
3. Render จะอ่าน `render.yaml` เจอ 2 อย่าง:
   - **web** `employee-hub-kpru` (Python, build `./build.sh`, start `gunicorn config.wsgi:application`)
   - **database** `employee-hub-db` (Postgres free)
4. กด **Apply** -> รอ Render สร้างทั้งคู่

> ถ้าชื่อ `employee-hub-kpru` ซ้ำ (เคยสร้างแล้ว) ให้ลบ service เก่าก่อน หรือแก้ `name` ใน `render.yaml` แล้ว push ใหม่

## 3. ดู Build Log
- หน้า Dashboard -> เลือก `employee-hub-kpru` -> **Logs**
- ต้องเห็น:
```
pip install -r requirements.txt
collectstatic -> 131 static files copied
migrate -> Applying employees.0001_initial OK
created admin/1234 หรือ admin password reset to 1234
```
- ถ้า error `ModuleNotFoundError` = `requirements.txt` ไม่ได้ install -> เช็ค `PYTHON_VERSION 3.12.8`
- ถ้า error `CSRF` ตอน login = `CSRF_TRUSTED_ORIGINS` ยังไม่ตั้ง -> เช็คว่า push ล่าสุดแล้ว

## 4. เปิดเว็บ + ทดสอบ
- URL: `https://employee-hub-kpru.onrender.com` (ดูใน Dashboard -> service URL)
- Login: `admin` / `1234`
- Smoke test:
  - [ ] Dashboard โหลดได้
  - [ ] เพิ่มพนักงานใหม่ (ใส่รูปได้)
  - [ ] แก้ไข / ลบ / ค้นหา (q, department, status)
  - [ ] Logout แล้ว login ใหม่ได้
- หมายเหตุ: รูปที่อัปโหลดเก็บใน `media/` บน disk ชั่วคราว -> **redeploy แล้วรูปหาย** (ตาม Q6 รับได้สำหรับทดสอบ) ถ้าจะเก็บถาวรต้องย้ายไป S3/Cloudinary ภายหลัง

## 5. ถ้า Deploy ไม่ผ่าน
- **Logs** ดูบรรทัดแดงแรกสุด
- **Manual Deploy** -> Clear build cache & Deploy
- เช็ค ENV ใน Dashboard -> Environment: `DEBUG=False`, `SECRET_KEY` auto-generated, `DATABASE_URL` linked จาก `employee-hub-db`
- สั่ง migrate เองผ่าน Render Shell: `python manage.py migrate` หรือ `python manage.py createsuperuser`

## 6. เปลี่ยนรหัส admin ภายหลัง (แนะนำ)
- Render Shell: `python manage.py shell`
```python
from django.contrib.auth import get_user_model
u=get_user_model().objects.get(username='admin')
u.set_password('รหัสใหม่ที่ปลอดภัย')
u.save()
```
- หรือแก้ `build.sh` ให้ใช้ ENV แล้ว redeploy

---
Push ล่าสุด: `git log --oneline -1` ต้องเป็น `00dd7cc` | Build: `./build.sh` idempotent | Prod: `DEBUG=False` + `CSRF_TRUSTED_ORIGINS`
