# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
import datetime

class UserProfile(models.Model):
    user = models.ForeignKey(User)
    phone = models.CharField(max_length = 11,null = True)
    balance = models.DecimalField(max_digits=5,decimal_places=2,default=0)
    points = models.IntegerField(default=0)


class Card(models.Model):
    number = models.IntegerField()
    password = models.CharField(max_length = 8)
    balance = models.DecimalField(max_digits = 5, decimal_places = 2)
    
    def __unicode__(self):
        return str(self.number)
        
class ResvNumber(models.Model):
    resv_number = models.IntegerField(default=0)
    
    def __unicode__(self):
        return str(self.resv_number)

def create_user_profile(sender=None, instance=None, created=True, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

models.signals.post_save.connect(create_user_profile, sender=User)


