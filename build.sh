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
    print("created admin/1234")
else:
    u = User.objects.get(username='admin')
    u.set_password('1234')
    u.is_superuser = True
    u.is_staff = True
    u.save()
    print("admin password reset to 1234")
PY