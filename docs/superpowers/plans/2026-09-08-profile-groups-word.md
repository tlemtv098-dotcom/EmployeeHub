# Profile + Groups + Word Report Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** เติม Profile ดู/แก้ + สิทธิ์ Admin/Member ให้ครบ 5 ข้อ แล้วออก Word ไทย 8-10 หน้าพร้อม ER/Flow วาง Desktop

**Estimated tasks:** 3 | **Estimated time:** ~60 min | **Touches:** Auth/Profile/Groups/Docs (forms, views, urls, templates, Word)

## Current Problem / Current Solution

- มีแล้ว: Register (`SignupForm` username/email/pass + `clean_email` กันซ้ำ), Login/Logout (`LoginView`/`LogoutView`), `@login_required` ทุกหน้า Employee, คอมเมนต์ไทย, หน้าสมัครไทย 100%
- ขาด: หน้า Profile ดู/แก้ของตัวเอง, แบ่งสิทธิ์ Admin/Member (Groups), Word พรีเซนต์อาจารย์
- `employees/urls.py` มี 8 path + signup, ยังไม่มี `profile/`, `templates/registration/` มีแค่ login/signup, `grep profile|Group` ไม่เจอ logic จริง

## Proposed Approach

- แนว A (เลือก): Profile ใช้ User มาตรฐาน + Groups แบบเบา + Word เต็ม — ไม่ migrate, ตรงใบงาน, ส่งอาจารย์ได้ทันที
- แนว B (ตัด): Profile ผูก Employee + Permissions รายตัว — ตรงสุดแต่ต้อง migrate + โค้ดเยอะ เสี่ยงส่งไม่ทัน
- แนวที่เลือกดีกว่าเพราะ: ไม่แตะ DB schema, สมัครใหม่เข้า Member ออโต้, Admin คือ is_staff/superuser, Word อ้างโค้ดจริงได้เลย

## Side by Side

| Scenario | Before | After |
| -------- | ------ | ----- |
| ดู/แก้ข้อมูลตัวเอง | ไม่มี ต้องเข้า /admin | มี /profile/ ดู + /profile/edit/ แก้ username/email/first/last |
| สมัครใหม่ได้สิทธิ์อะไร | ได้ User เปล่า ไม่มีกลุ่ม | เข้า Group Member ออโต้, ดู/เพิ่มพนักงานได้ |
| ลบ/แก้พนักงาน | ใคร login ก็ทำได้ | Member ทำไม่ได้ (403), Admin/staff ทำได้ |
| ส่งอาจารย์ | มีแค่ PPT/PDF 6 สไลด์ | มี Word 8-10 หน้า ไทย ปก สารบัญ ER Flow สาธิต โค้ด ฝังภาพ |

## Assumptions & Risks

- **Assumed:** ใช้ `django.contrib.auth.models.User + Group` เดิม ไม่สร้าง Custom User/Profile model (Q14=A, Q15=A)
- **Assumed:** เปิดสมัครเองทุกคน (Q9=A เดิม), สมัครเสร็จไป /login/ ไม่ auto-login (Q11=B เดิม)
- **Assumed:** Word ภาษาไทย 8-10 หน้า ชื่อ `EmployeeHub_รายงานโครงสร้างระบบ.docx` วาง Desktop + ฝังภาพ ER/Flow (Q16=A, Q17=A)
- **Risk:** ถ้าอาจารย์อยากเห็น Permissions รายตัว แนว A จะดูเบา -> รับมือด้วยตาราง Groups/Permissions ใน Word + โค้ด `permission_required` ตรง delete
- **Risk:** python-docx ไม่มี + เน็ตช้า install นาน -> fallback สร้าง .docx ผ่าน COM Word หรือ HTML-save-as-docx
- **Risk:** แก้ delete ให้ staff-only อาจทำ demo member ลบไม่ผ่าน -> ต้องมีข้อความ 403 ไทยชัดเจน + สอนใน Word

## Impact

- ครบ 5 ข้อใบงาน: validation + login/logout + profile + login_required + groups
- Demo อาจารย์ลื่น: สมัคร -> login -> protected -> แก้โปรไฟล์ -> สิทธิ์ -> logout
- Word พร้อมส่ง: ปก คำนำ สารบัญ ER User/Employee Flow สาธิต โค้ด Tech

---

## Task Overview

> **For implementation tasks:** REQUIRED SUB-SKILL: Use superpowers:test-driven-development before editing production code. Each task is a RED -> GREEN -> REFACTOR slice.
> **Parallel-first:** Spawn separate sub-agents for independent lanes. Do not parallelize tasks that can race on the same files, migrations, generated artifacts, fixtures, or shared state.

1. **[Profile View/Edit]** - Lane A | Can run together: none (แตะ forms/views/urls เดียวกัน) | Must wait for: none | TDD slice: `test_profile_requires_login_and_updates_email` -> ProfileForm+views -> `manage.py test`
2. **[Groups Admin/Member]** - Lane A | Can run together: none | Must wait for: Task 1 (แก้ signup เดียวกัน) | TDD slice: `test_signup_joins_member_and_delete_requires_admin` -> groups+decorators -> `manage.py test`
3. **[Word Report TH 8-10p]** - Lane B | Can run together: Task 1, Task 2 (อ่านโค้ดหลังเสร็จดีสุด) | Must wait for: Task 1+2 | TDD slice: docs-only -> เปิด docx ครบ 8-10 หน้า + ภาพ ER/Flow -> verify

---

### Task 1: Profile View/Edit

**Files:**

- Modify: `D:\EmployeeHub-main\employees\forms.py` (เพิ่ม ProfileForm)
- Modify: `D:\EmployeeHub-main\employees\views.py` (เพิ่ม profile, profile_edit)
- Modify: `D:\EmployeeHub-main\employees\urls.py` (เพิ่ม profile/, profile/edit/)
- Create: `D:\EmployeeHub-main\templates\registration\profile.html`
- Create: `D:\EmployeeHub-main\templates\registration\profile_edit.html`
- Test: `D:\EmployeeHub-main\employees\tests.py` (หรือ `employees/tests/test_auth.py`)

**Parallelization:**

- Can run with: none
- Must wait for: none
- Race risk: `forms.py/views.py/urls.py` ชน Task 2 -> ห้ามขนาน

- [ ] **Step 0: Load the TDD discipline**

Use `superpowers:test-driven-development` before editing production code. This task must follow RED -> GREEN -> REFACTOR.

- [ ] **Step 1: Write the failing test**

```python
def test_profile_requires_login():
    c = Client()
    assert c.get("/profile/").status_code == 302

def test_profile_updates_email():
    c = Client()
    c.create_user = User.objects.create_user("u1","u1@x.com","Test12345!")
    c.login(username="u1", password="Test12345!")
    r = c.post("/profile/edit/", {"username":"u1","email":"new@x.com","first_name":"Som","last_name":"Chai"})
    assert r.status_code == 302
    assert User.objects.get(username="u1").email == "new@x.com"
```

- [ ] **Step 2: Run the test and confirm it fails for the expected reason**

Run `py manage.py test employees -v 2`. Expected: FAIL 404 `/profile/` not found, not syntax error.

- [ ] **Step 3: Implement the minimal code**

`forms.py` เพิ่ม `ProfileForm(forms.ModelForm)` fields `username,email,first_name,last_name` + `clean_email` กันซ้ำยกเว้นตัวเอง. `views.py` เพิ่ม `@login_required def profile` render + `profile_edit` save + messages ไทย. `urls.py` เพิ่ม 2 path. Templates ก็อปโครง `login-card` ไทย.

- [ ] **Step 4: Run the test and confirm it passes**

Run same `py manage.py test employees -v 2`. Expected: PASS, `check` clean.

- [ ] **Step 5: Refactor only after green**

จัด label ไทย, ลิงก์ sidebar โปรไฟล์, `messages` ไทย.

---

### Task 2: Groups Admin/Member

**Files:**

- Modify: `D:\EmployeeHub-main\employees\views.py` (signup เข้ากลุ่ม Member, delete/update กันสิทธิ์)
- Modify: `D:\EmployeeHub-main\employees\urls.py` (ไม่เพิ่ม path, แค่ guard)
- Modify: `D:\EmployeeHub-main\employees\apps.py` (ready สร้าง Group Member + permissions view/add)
- Test: `D:\EmployeeHub-main\employees\tests.py` เพิ่มเคส groups

**Parallelization:**

- Can run with: none
- Must wait for: Task 1 (แก้ `views.py`/`forms.py` ไฟล์เดียวกัน)
- Race risk: same files `views.py` + shared `Group` state

- [ ] **Step 0: Load the TDD discipline**

Use `superpowers:test-driven-development` before editing production code. RED -> GREEN -> REFACTOR.

- [ ] **Step 1: Write the failing test**

```python
def test_signup_joins_member():
    c = Client()
    c.post("/signup/", {"username":"m1","email":"m1@x.com","password1":"Test12345!","password2":"Test12345!"})
    assert Group.objects.get(name="Member").user_set.filter(username="m1").exists()

def test_delete_requires_admin():
    member_login_client.post("/employees/1/delete/")
    assert response.status_code == 403
    admin_client.post("/employees/1/delete/")
    assert response.status_code == 302
```

- [ ] **Step 2: Run the test and confirm it fails**

`py manage.py test employees -v 2` FAIL `Group Member DoesNotExist` / delete 302 ทั้งคู่ (ยังไม่ guard).

- [ ] **Step 3: Implement the minimal code**

`apps.py ready`: `Group.objects.get_or_create(name="Member")` + ใส่ `view_employee, add_employee`. `signup`: `user.groups.add(Member)`. `employee_delete` (+ `employee_update` ถ้าต้องการ): `@user_passes_test(lambda u: u.is_staff or u.is_superuser)` หรือ `permission_required` + เทมเพลต 403 ไทย. ไม่แตะ Employee model.

- [ ] **Step 4: Run the test and confirm it passes**

Same test PASS. `py manage.py check` PASS.

- [ ] **Step 5: Refactor only after green**

เพิ่ม badge สิทธิ์ใน base/sidebar, ข้อความ 403 ไทย, `admin/1234` เป็น superuser อยู่แล้ว.

---

### Task 3: Word Report TH 8-10p

**Files:**

- Create: `C:\Users\Admin\Desktop\EmployeeHub_รายงานโครงสร้างระบบ.docx` (หลัก ส่งอาจารย์)
- Create: `D:\EmployeeHub-main\docs\EmployeeHub_รายงานโครงสร้างระบบ.docx` (สำเนาใน repo)
- Modify: `D:\EmployeeHub-main\README.md` (ลิงก์ไฟล์ Word ถ้าจำเป็น)
- Test: เปิดไฟล์จริง (docs-only exception)

**Parallelization:**

- Can run with: Task 1, Task 2 (draft ได้) แต่ final ต้องรอโค้ดจริง
- Must wait for: Task 1, Task 2 (ER/Flow/โค้ดต้องตรง)
- Race risk: none (ไฟล์ docx แยก) ยกเว้น README ถ้าแก้พร้อมกัน

- [ ] **Step 0: Load the TDD discipline**

This task is docs/config-only; no behavior test. Verification = เปิด docx อ่านครบ + ภาพขึ้น + ไทยไม่เพี้ยน + 8-10 หน้า.

- [ ] **Step 1: Write the failing test (checklist)**

```
- [ ] ปก ชื่อ วิชา ผู้จัดทำ tlemtv098@gmail.com KPRU วัน
- [ ] สารบัญ คำนำ วัตถุประสงค์ ขอบเขต
- [ ] ER auth_user + employees_employee (ตาราง + ภาพ)
- [ ] Flow register/login/protected/logout + validation + login_required + groups
- [ ] สาธิต 4 ขั้นพร้อมคำสั่ง/ภาพ
- [ ] โค้ดสำคัญ SignupForm/ProfileForm/signup/profile/groups
- [ ] Tech + URLs + วิธีรัน + สรุป
- [ ] 8-10 หน้า ฟอนต์ TH Sarabun/Kanit/Prompt
```

- [ ] **Step 2: Run the test and confirm it fails**

`Test-Path Desktop docx` = False. ถือว่า FAIL.

- [ ] **Step 3: Implement the minimal code**

ใช้ `python-docx` (fallback COM): สร้างปก สารบัญ วัตถุประสงค์ ER (ตาราง auth_user 11 ฟิลด์ + Employee 14 ฟิลด์ + ภาพ ER/Flow จาก matplotlib/PIL วาดกล่องไทย) Flow 4 ขั้น สาธิต copy-paste ได้ โค้ดบล็อกสั้น Tech table. ฟอนต์ไทย หัว Kanit เนื้อหา TH Sarabun. เซฟ 2 ที่ (Desktop + docs/).

- [ ] **Step 4: Run the test and confirm it passes**

เปิด docx: ครบ checklist, 8-10 หน้า, ภาพ ER/Flow ขึ้น, ไทยไม่ `????`, `git status` เห็นสำเนา.

- [ ] **Step 5: Refactor only after green**

ย่อคำซ้ำ จัดเลขหน้า หัว/ท้าย ใส่ GitHub/Render/admin-1234 หมายเหตุ media หาย.

