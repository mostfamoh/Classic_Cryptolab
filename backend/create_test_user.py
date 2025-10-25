#!/usr/bin/env python
"""Create a test user for testing login."""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cryptolab.settings')
django.setup()

from users.models import User

# Create test users
try:
    # Student user
    if not User.objects.filter(username='student').exists():
        user1 = User.objects.create_user(
            username='student',
            email='student@test.com',
            password='student123',
            role='student',
            first_name='Test',
            last_name='Student'
        )
        print(f"✅ Created student user: username='student', password='student123'")
    else:
        print("⚠️  Student user already exists")
    
    # Instructor user
    if not User.objects.filter(username='instructor').exists():
        user2 = User.objects.create_user(
            username='instructor',
            email='instructor@test.com',
            password='instructor123',
            role='instructor',
            first_name='Test',
            last_name='Instructor'
        )
        print(f"✅ Created instructor user: username='instructor', password='instructor123'")
    else:
        print("⚠️  Instructor user already exists")
    
    print("\n📋 Total users in database:", User.objects.count())
    print("\n🎯 You can now login with:")
    print("   Username: student | Password: student123")
    print("   Username: instructor | Password: instructor123")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
