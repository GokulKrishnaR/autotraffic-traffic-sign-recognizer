
from django.db import models
class User(models.Model):
    uname=models.CharField(max_length=100,blank=True)
    uaddress=models.CharField(max_length=100,blank=True)
    ucontact=models.CharField(max_length=100,blank=True)
    uemail=models.CharField(max_length=100,blank=True)
    upassword=models.CharField(max_length=100,blank=True)
class Login(models.Model):
    username=models.CharField(max_length=100,blank=True)
    password=models.CharField(max_length=100,blank=True)
    usertype=models.CharField(max_length=100,blank=True)