import getpass
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'create gum super user'

    def handle(self, *args, **options):
        User = get_user_model()
        username = input("Username: ")
        email = input("Email address:")
        full_name = input("Full name:")
        date_of_birth = input("Date of birth (YYYY-MM-DD): ")
        phone_number = input("Phone number: +380")
        gender = "default"
        status = "main manager"
        while True:
            password = getpass.getpass('Password: ')
            password2 = getpass.getpass('Password (again): ')
            if password != password2:
                self.stdout.write(self.style.ERROR("Passwords do not match. Try again."))
            elif password.strip() == '':
                self.stdout.write(self.style.ERROR("Password cannot be blank."))
            else:
                break

        user = User.objects.create_user(
            username=username,
            email=email,
            full_name=full_name,
            date_of_birth=date_of_birth,
            phone_number=phone_number,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save()
        self.stdout.write(self.style.SUCCESS("✅ GUM main manager created successfully!"))