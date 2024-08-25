from django.db import models

# Create your models here.
from email.policy import default
from django.contrib.auth.models import User

from localflavor.in_.forms import *

from .utils import user_directory_path
import random


class Location(models.Model):
    address_1 = models.CharField(max_length=128,blank=True)
    address_2 = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=64)
    STATE_CHOICES = (('KA', 'Karnataka'), ('AP', 'Andhra Pradesh'), ('KL', 'Kerala'), ('TN', 'Tamil Nadu'), ('MH', 'Maharashtra'), ('UP', 'Uttar Pradesh'), ('GA', 'Goa'), ('GJ', 'Gujarat'), ('RJ', 'Rajasthan'), ('HP', 'Himachal Pradesh'), ('TG', 'Telangana'), ('AR', 'Arunachal Pradesh'), ('AS', 'Assam'), ('BR', 'Bihar'), ('CT', 'Chhattisgarh'), ('HR', 'Haryana'), ('JH', 'Jharkhand'), ('MP', 'Madhya Pradesh'), ('MN', 'Manipur'), ('ML', 'Meghalaya'), ('MZ', 'Mizoram'), ('NL', 'Nagaland'), ('OR', 'Odisha'), ('PB', 'Punjab'), ('SK', 'Sikkim'), ('TR', 'Tripura'), ('UT', 'Uttarakhand'), ('WB', 'West Bengal'), ('AN', 'Andaman and Nicobar Islands'), ('CH', 'Chandigarh'), ('DH', 'Dadra and Nagar Haveli and Daman and Diu'), ('DL', 'Delhi'), ('JK', 'Jammu and Kashmir'), ('LD', 'Lakshadweep'), ('LA', 'Ladakh'), ('PY', 'Puducherry'))
    state = models.CharField(max_length=2, choices=STATE_CHOICES)
    zip_code = models.CharField(max_length=8)
    

    def __str__(self):
        return f'Location {self.id}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=user_directory_path, null=True)
    bio = models.CharField(max_length=140, blank=True)
    phone_number = models.CharField(max_length=12, blank=True)
    location = models.OneToOneField(
        Location, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.user.username}\'s Profile'
    





