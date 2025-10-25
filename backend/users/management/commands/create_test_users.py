from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):
    help = 'Creates default test users for the application'

    def handle(self, *args, **options):
        # Create student user
        if not User.objects.filter(username='student').exists():
            User.objects.create_user(
                username='student',
                email='student@test.com',
                password='student123',
                role='student',
                first_name='Test',
                last_name='Student'
            )
            self.stdout.write(self.style.SUCCESS('✅ Created student user (username: student, password: student123)'))
        else:
            self.stdout.write(self.style.WARNING('⚠️  Student user already exists'))

        # Create instructor user
        if not User.objects.filter(username='instructor').exists():
            User.objects.create_user(
                username='instructor',
                email='instructor@test.com',
                password='instructor123',
                role='instructor',
                first_name='Test',
                last_name='Instructor'
            )
            self.stdout.write(self.style.SUCCESS('✅ Created instructor user (username: instructor, password: instructor123)'))
        else:
            self.stdout.write(self.style.WARNING('⚠️  Instructor user already exists'))

        # Create admin superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@test.com',
                password='admin123',
                role='instructor',
                first_name='Admin',
                last_name='User'
            )
            self.stdout.write(self.style.SUCCESS('✅ Created admin superuser (username: admin, password: admin123)'))
        else:
            self.stdout.write(self.style.WARNING('⚠️  Admin user already exists'))

        self.stdout.write(self.style.SUCCESS('\n🎉 Setup complete! You can login with:'))
        self.stdout.write('   Student: student / student123')
        self.stdout.write('   Instructor: instructor / instructor123')
        self.stdout.write('   Admin: admin / admin123')
