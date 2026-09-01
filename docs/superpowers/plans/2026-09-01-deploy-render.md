# EmployeeHub Render Deploy Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** ดัน EmployeeHub ขึ้น Render แบบ Blueprint ให้รันได้จริงด้วย admin/1234

**Estimated tasks:** 4 | **Estimated time:** ~30 min | **Touches:** git/GitHub, config/settings, build.sh, render.yaml/docs

## Current Problem / Current Solution

- โค้ดอยู่ local `D:\EmployeeHub-main` ยังไม่เป็น git repo (`git status` = fatal not a git repository)
- มี `render.yaml` พร้อม (service `employee-hub-kpru` + `employee-hub-db`) และ `build.sh` ที่ hardcode ลบ/สร้าง admin/1234 ทุกครั้ง
- `config/settings.py` ใช้ `DEBUG=True` default และ `ALLOWED_HOSTS` มีแค่ localhost + RENDER_EXTERNAL_HOSTNAME, ยังไม่ตั้ง `DEBUG=False` บน prod, ไม่มี `CSRF_TRUSTED_ORIGINS`
- ยังไม่ push ขึ้น `https://github.com/tlemtv098-dotcom/EmployeeHub` เลยเชื่อม Render Blueprint ไม่ได้

## Proposed Approach

- Init git local, commit ทั้งโปรเจกต์, push ขึ้น GitHub `tlemtv098-dotcom/EmployeeHub` (branch main)
- ปรับ `build.sh` ให้ idempotent (ไม่ลบ user ทุกครั้ง, ใช้ get_or_create + set_password) แต่ยังใช้ admin/1234 ตามที่ user เลือก (A)
- เติม `DEBUG=False` และ `ALLOWED_HOSTS` / `CSRF` ให้พร้อม prod แบบไม่ทำลาย local dev, ใส่ `PYTHON_VERSION` ตาม render.yaml เดิม
- Deploy แบบ Blueprint (render.yaml) แล้ว smoke test login + CRUD ทดสอบ media ephemeral รับได้

## Side by Side

| Scenario | Before | After |
| -------- | ------ | ----- |
| Git state | ไม่มี .git, push ไม่ได้ | มี .git, remote origin ชี้ EmployeeHub, push main สำเร็จ |
| Admin บน Render | `build.sh` ลบ admin ทุก deploy, hardcode | สร้างถ้าไม่มี, อัปรหัส 1234 แบบ idempotent ไม่ลบข้อมูลอื่น |
| Prod settings | DEBUG=True, ALLOWED_HOSTS ไม่ครอบคลุม | DEBUG จาก ENV (default True local, False บน Render ถ้าตั้ง), ALLOWED_HOSTS รองรับ Render host + CSRF |
| Deploy | ยังไม่เชื่อม Render | Blueprint สร้าง web+DB จาก render.yaml, เข้า URL ได้, login admin/1234 ได้ |

## Assumptions & Risks

- **Assumed:** user มีสิทธิ์ push ไป `tlemtv098-dotcom/EmployeeHub` และมี GitHub token/PAT พร้อมใช้บนเครื่องนี้ (Task 1 ต้องใช้)
- **Assumed:** Render free plan ยังสร้าง DB `employee-hub-db` ได้ (ฟรีมีโควตา 90 วัน)
- **Assumed:** user ยอมรับ `admin/1234` อ่อนแอสำหรับทดสอบ และยอมรับรูปหายเมื่อ redeploy (Q6 = A)
- **Risk:** ถ้าไม่มี token จะ push ไม่ผ่าน -> task 1 บล็อก, ต้อง fallback ให้คำสั่ง manual ไปรันเอง
- **Risk:** Blueprint ชื่อ `employee-hub-kpru` ซ้ำกับของเดิมบน Render จะสร้างไม่ผ่าน -> ต้องเปลี่ยน name
- **Risk:** `Pillow` + `whitenoise` collectstatic บน Render อาจ fail ถ้า STATIC ผิด

## Impact

- Push ครั้งแรกทำให้ต่อ Render ได้ทันที
- Build idempotent ลดเสี่ยงลบ user อื่นที่ชื่อ admin ซ้ำ
- Prod settings ปลอดภัยขึ้นโดยไม่กระทบ local dev
- มีคู่มือคลิก Blueprint ให้ user ทำซ้ำได้

---

## Task Overview

> **For implementation tasks:** REQUIRED SUB-SKILL: Use superpowers:test-driven-development before editing production code. Each task is a RED -> GREEN -> REFACTOR slice.
> **Parallel-first:** Spawn separate sub-agents for independent lanes. Do not parallelize tasks that can race on the same files, migrations, generated artifacts, or shared state.

1. **[Git init + push GitHub]** - Lane A | Can run together: none (ต้องทำก่อน Blueprint) | Must wait for: none | TDD slice: config-only -> `git log --oneline -1` + `git remote -v` ผ่าน
2. **[Harden build.sh admin idempotent]** - Lane B | Can run together: Task 3 | Must wait for: Task 1 (commit เดียวกันได้) | TDD slice: config-only -> `bash -n build.sh` + dry-run shell ผ่าน
3. **[Prod settings patch]** - Lane B | Can run together: Task 2 | Must wait for: none (แก้คนละไฟล์) | TDD slice: config-only -> `python manage.py check --deploy` + `collectstatic --noinput` ผ่าน
4. **[Blueprint deploy guide + smoke test]** - Lane C | Can run together: none | Must wait for: Task 1,2,3 | TDD slice: docs-only -> คู่มือ + checklist ทดสอบ login/CRUD

---

### Task 1: Git init + push GitHub

**Files:**

- Modify: `D:\EmployeeHub-main\.git` (create via git init)
- Modify: `D:\EmployeeHub-main\.gitignore` (verify ครอบคลุม .venv/db.sqlite3/media)
- Test: ไม่มี test file - config-only, verify ด้วย git commands

**Parallelization:**

- Can run with: none (ต้องเสร็จก่อน task 4)
- Must wait for: none
- Race risk: none (ไฟล์ใหม่)

- [ ] **Step 0: Load the TDD discipline**

Use `superpowers:test-driven-development` before editing production code. This task is docs/config-only; explain why failing behavior test is not appropriate: ไม่มี business logic ใหม่, แค่ git plumbing ต้อง verify ด้วย git commands.

- [ ] **Step 1: Write the failing test (config check)**

```bash
git status  # expect fatal: not a git repository (ก่อนแก้)
git remote -v # expect empty
```

- [ ] **Step 2: Run the test and confirm it fails for the expected reason**

รัน `git status` ใน `D:\EmployeeHub-main` ต้องได้ fatal not a git repo ตามที่ตรวจแล้ว

- [ ] **Step 3: Implement the minimal code**

```powershell
cd D:\EmployeeHub-main
git init
git add .
git commit -m "Initial commit: EmployeeHub Django app"
git branch -M main
git remote add origin https://github.com/tlemtv098-dotcom/EmployeeHub.git
git push -u origin main
# ถ้า push ต้อง auth ให้ใช้ PAT: git remote set-url origin https://<PAT>@github.com/tlemtv098-dotcom/EmployeeHub.git
```

ถ้าไม่มี gh/token ให้ fallback: ส่งคำสั่งชุดนี้ให้ user รันเองพร้อมวิธีสร้าง PAT

- [ ] **Step 4: Run the test and confirm it passes**

```bash
git log --oneline -1  # ต้องเห็น Initial commit
git remote -v  # ต้องเห็น origin -> EmployeeHub.git
git status  # clean
# เปิด https://github.com/tlemtv098-dotcom/EmployeeHub บน browser ต้องเห็นโค้ด
```

- [ ] **Step 5: Refactor only after green**

ลบ credential ที่ฝัง PAT ออกจาก remote URL หลัง push (ถ้าใส่): `git remote set-url origin https://github.com/tlemtv098-dotcom/EmployeeHub.git`

---

### Task 2: Harden build.sh admin idempotent

**Files:**

- Modify: `D:\EmployeeHub-main\build.sh`
- Test: `bash -n build.sh` (syntax check) + manual dry-run

**Parallelization:**

- Can run with: Task 3 (คนละไฟล์)
- Must wait for: Task 1 (ควร commit พร้อมกัน แต่แก้ไฟล์แยกทำขนานได้)
- Race risk: none (แก้ไฟล์เดียว)

- [ ] **Step 0: Load the TDD discipline**

config-only: ไม่มี python behavior test, verify ด้วย shell syntax + Django shell logic

- [ ] **Step 1: Write the failing test**

Current `build.sh` ลบ admin ทุกครั้ง:
```bash
User.objects.filter(username='admin').delete(); User.objects.create_superuser('admin', 'admin@example.com', '1234')
```
ถือว่า fail ด้าน idempotent + เสี่ยงลบข้อมูล

- [ ] **Step 2: Run the test and confirm it fails**

`cat build.sh` ต้องเห็นบรรทัด delete/create ตามเดิม

- [ ] **Step 3: Implement the minimal code**

แก้ `build.sh` เป็น idempotent แต่ยังใช้ admin/1234 ตาม Q3=A:

```bash
#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py shell << 'PY'
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', '1234')
else:
    u = User.objects.get(username='admin')
    u.set_password('1234')
    u.is_superuser = True
    u.is_staff = True
    u.save()
    print("admin password reset to 1234")
PY
```

ยังคง hardcode ตาม user เลือก แต่ไม่ลบทุกครั้ง

- [ ] **Step 4: Run the test and confirm it passes**

```bash
bash -n build.sh  # syntax ok
# local dry-run (ถ้ามี venv):
python manage.py shell -c "from django.contrib.auth import get_user_model; print('shell ok')"
```

- [ ] **Step 5: Refactor only after green**

ตรวจสอบว่าไฟล์มี execute permission และ line ending LF

---

### Task 3: Prod settings patch

**Files:**

- Modify: `D:\EmployeeHub-main\config\settings.py`
- Modify: `D:\EmployeeHub-main\render.yaml` (เพิ่ม ENV DEBUG=False, PYTHON_VERSION)
- Test: `python manage.py check --deploy` (ถ้า --deploy เตือนเกินไป ใช้ `check` ปกติ)

**Parallelization:**

- Can run with: Task 2
- Must wait for: none
- Race risk: none (คนละไฟล์กับ Task 2)

- [ ] **Step 0: Load the TDD discipline**

config-only: verify ด้วย Django system check

- [ ] **Step 1: Write the failing test**

```bash
python manage.py check  # ตอนนี้ผ่านแต่ check --deploy จะเตือน DEBUG=True, SECRET_KEY weak
grep -n "DEBUG" config/settings.py  # เห็น DEBUG default True
```

- [ ] **Step 2: Run the test and confirm it fails**

รัน `python manage.py check --deploy` ต้องเตือนเรื่อง DEBUG/ALLOWED_HOSTS/SECRET_KEY

- [ ] **Step 3: Implement the minimal code**

Patch `config/settings.py` minimal:

```python
# DEBUG จาก ENV เหมือนเดิมแต่เพิ่ม comment ให้ Render ตั้ง DEBUG=False
DEBUG = os.environ.get("DEBUG", "True").lower() == "true"

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
render_host = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if render_host:
    ALLOWED_HOSTS.append(render_host)
# เพิ่ม CSRF สำหรับ https ของ Render
CSRF_TRUSTED_ORIGINS = []
if render_host:
    CSRF_TRUSTED_ORIGINS.append(f"https://{render_host}")
```

Patch `render.yaml` เพิ่ม env:

```yaml
envVars:
  - key: PYTHON_VERSION
    value: 3.12.8
  - key: SECRET_KEY
    generateValue: true
  - key: DEBUG
    value: False
  - key: DATABASE_URL
    fromDatabase:
      name: employee-hub-db
      property: connectionString
```

ไม่เปลี่ยน logic อื่น

- [ ] **Step 4: Run the test and confirm it passes**

```bash
python manage.py check
python manage.py collectstatic --noinput  # ต้องผ่านด้วย whitenoise
```

- [ ] **Step 5: Refactor only after green**

ลบ import ไม่ใช้ถ้ามี, รัน `python -m py_compile config/settings.py`

---

### Task 4: Blueprint deploy guide + smoke test

**Files:**

- Create: `D:\EmployeeHub-main\docs\DEPLOY_RENDER.md`
- Test: manual smoke test checklist (docs-only)

**Parallelization:**

- Can run with: none
- Must wait for: Task 1,2,3 (ต้อง push โค้ดที่แก้แล้วก่อน)
- Race risk: none

- [ ] **Step 0: Load the TDD discipline**

docs-only: ไม่มี code behavior, verify ด้วยการอ่านคู่มือแล้วทำตามได้

- [ ] **Step 1: Write the failing test**

ยังไม่มี `docs/DEPLOY_RENDER.md` -> นับว่า fail

- [ ] **Step 2: Run the test and confirm it fails**

`Test-Path docs/DEPLOY_RENDER.md` -> False

- [ ] **Step 3: Implement the minimal code**

สร้าง `docs/DEPLOY_RENDER.md` ภาษาไทย ครอบคลุม:

1. วิธี push (คำสั่ง git)
2. วิธีสร้าง Blueprint บน Render (New -> Blueprint -> เลือก repo -> Apply)
3. รอ build log ดู `collectstatic` + `migrate` + `admin password reset`
4. เปิด URL `https://employee-hub-kpru.onrender.com` -> login admin/1234 -> ทดสอบ เพิ่ม/แก้ไข/ลบพนักงาน, อัปรูป
5. วิธีดู log ถ้า fail, วิธี redeploy, วิธีเปลี่ยนรหัส admin ภายหลัง
6. หมายเหตุรูปหายเมื่อ redeploy (Q6)

- [ ] **Step 4: Run the test and confirm it passes**

เปิดไฟล์อ่านแล้วทำตามได้, ลิงก์ render.yaml ตรง

- [ ] **Step 5: Refactor only after green**

ย่อให้กระชับ, ใส่ screenshot placeholder, ใส่คำสั่ง PowerShell block ให้ copy ได้
