import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'accounts_service.settings')
django.setup()

from accounts.models import User

try:
    user, created = User.objects.get_or_create(email="admin@admin.com")
    user.set_password("admin123")
    user.is_active = True
    user.is_staff = True
    user.is_admin = True
    user.firstname = "Super"
    user.lastname = "Admin"
    user.save()
    
    print(f"Admin user {'created' if created else 'updated'}: admin@admin.com / admin123")

except Exception as e:
    print(f"Error: {e}")
