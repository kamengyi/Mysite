from django.db import models
from phone_field import PhoneField

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=50, unique=True) 
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=256)
    tel = PhoneField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    has_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-created']
        verbose_name = '用户'
        verbose_name_plural = '用户'


class ConfirmString(models.Model):
    code = models.CharField(max_length=256)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user + ": " + self.code

    class Meta:
        ordering = ['-created']
        verbose_name = '注册码'
        verbose_name_plural = '注册码'

