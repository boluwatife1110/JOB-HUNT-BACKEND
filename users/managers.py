from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, user_type=None, phone_number=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(
            email=email, 
            first_name=first_name, 
            last_name=last_name, 
            user_type=user_type, 
            phone_number=phone_number, 
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        # We manually provide these because createsuperuser won't prompt for them by default
        return self.create_user(
            email, 
            first_name, 
            last_name, 
            password, 
            user_type='admin', # Or whatever your admin type is
            phone_number='0000000000', 
            **extra_fields
        )