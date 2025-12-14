import os
import django
import sys

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'accounts_service.settings')
django.setup()

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import User

def test_login():
    print("--- Starting Login Verification ---")
    
    # 1. Check User Existence
    try:
        user = User.objects.get(email="admin@admin.com")
        print(f"User found: {user.email}, Admin: {user.is_admin}, Active: {user.is_active}")
        print(f"Password Check ('admin123'): {user.check_password('admin123')}")
    except User.DoesNotExist:
        print("CRITICAL: Admin user NOT found!")
        return

    # 2. Test Authenticate
    print("\nExecuting authenticate(email='admin@admin.com', password='admin123')...")
    try:
        auth_user = authenticate(email="admin@admin.com", password="admin123")
        if auth_user:
            print("Authentication SUCCESSFUL.")
        else:
            print("Authentication FAILED (Returned None).")
            return
    except Exception as e:
        print(f"Authentication CRASHED: {e}")
        import traceback
        traceback.print_exc()
        return

    # 3. Test Token Generation
    print("\nGenerating Token...")
    try:
        refresh = RefreshToken.for_user(auth_user)
        refresh['email'] = auth_user.email
        refresh['is_admin'] = auth_user.is_admin
        refresh['is_staff'] = auth_user.is_staff
        
        print(f"Refresh Token: {str(refresh)[:20]}...")
        print(f"Access Token: {str(refresh.access_token)[:20]}...")
    except Exception as e:
        print(f"Token Generation CRASHED: {e}")
        import traceback
        traceback.print_exc()
        return

    print("\n--- Verification Complete: ALL SYSTEMS GO ---")

if __name__ == "__main__":
    test_login()
