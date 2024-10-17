from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuarios(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    cpf = models.EmailField(max_length=11, unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']