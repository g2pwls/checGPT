from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=100,blank=True)
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)
    interests = models.CharField(max_length=100, blank=True, verbose_name='관심 장르')

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
