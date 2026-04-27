from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager


class User(AbstractUser):
    USER_CHOICES = (
        ('job_seeker', 'Job Seeker'),
        ('recruiter', 'Recruiter'),
    )

    profile_image = models.ImageField(
        upload_to='profile_images/',
        null=True,
        blank=True
    )

    user_type = models.CharField(
        max_length=15,
        choices=USER_CHOICES,
        default='job_seeker'
    )

    first_name = models.CharField(max_length=40, blank=True, null=True)
    last_name = models.CharField(max_length=40, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'user_type', 'phone_number']

    objects = UserManager()


class JobSeekerProfile(models.Model):
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    experience = models.TextField(blank=True)


    def __str__(self):
        return f"{self.user.email} - Job Seeker"


class RecruiterProfile(models.Model):
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    company_website = models.URLField(blank=True)

    def __str__(self):
        return f"{self.user.email} - Recruiter"