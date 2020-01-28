from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Create your models here.
class UserProfileManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, contact, password=None):
        if not email:
            raise ValueError('User must have an email address!')
        email=self.normalize_email(email)
        user=self.model(email=email, first_name=first_name, last_name=last_name, contact=contact)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, contact, password):
        user=self.create_user(email, first_name, last_name, contact, password)
        user.is_superuser=True
        user.is_staff=True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser, PermissionsMixin):
    email=models.EmailField(max_length=255, unique=True)
    first_name=models.CharField(max_length=150)
    last_name=models.CharField(max_length=150)
    contact=models.BigIntegerField()
    discription=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    dob=models.DateField(null=True)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)

    objects=UserProfileManager()

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['first_name', 'last_name','contact']

    def get_full_name(self):
        return self.first_name+" "+self.last_name

    def __str__(self):
        return self.email
