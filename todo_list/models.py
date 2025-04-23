import os
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.timezone import now
from django.conf import settings


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email)
        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


class Task(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
    ]

    CATEGORY_CHOICES = [
        ('Work', 'Work'),
        ('Personal', 'Personal'),
        ('Urgent', 'Urgent'),
    ]

    name = models.CharField(max_length=255)
    time_period = models.CharField(max_length=100)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default="Personal")
    priority = models.IntegerField(default=1)  # 1 = Low, 2 = Medium, 3 = High
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="assigned_tasks"
    )

    def __str__(self):
        return f"{self.name} ({self.status})"


def user_static_path(instance, filename):
    return f"static/profile_images/{instance.user.username}_{filename}"


class UserProfile(models.Model):
    user = models.OneToOneField(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name="profile"
    )
    full_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(
        max_length=10,
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],
        blank=True,
        null=True
    )
    bio = models.TextField(blank=True, null=True)
    hobbies = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(
        upload_to=user_static_path, 
        default="static/profile_images/default.png", 
        blank=True, 
        null=True
    )

    def __str__(self):
        return self.user.username
