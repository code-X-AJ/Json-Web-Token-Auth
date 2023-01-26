from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# this is custom user model 
class User(AbstractUser):
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


# this is the model for image handeling
class Picture(models.Model):
    name = models.CharField(max_length=255, blank=True)
    picture = models.ImageField(upload_to="pictures")


