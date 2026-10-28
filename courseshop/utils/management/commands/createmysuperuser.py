from accounts.models import User 
from django.core.management import BaseCommand, CommandError
  
  
class Command(BaseCommand):
    help = 'create super user with with username set'

    def handle(self, *args, **options):
        phone_number = input("Phone Number: ")
        email = input("Email address: ")
        password = input("Password: ")
        confirm_password = input("Confirm password: ")

        if password != confirm_password:
            raise CommandError("Passwords don't match.")

        User.objects.create_superuser(phone_number=phone_number, username=phone_number, email=email, password=password)
        self.stdout.write(
            self.style.SUCCESS('Successfully created the user.')
        )