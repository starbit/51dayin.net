#!/usr/bin/env python
import random
import string
from django.dispatch import dispatcher
from django.db.models.signals import post_syncdb
from django.dispatch import receiver
from models import Card, ResvNumber
from user import models as userapp
import os
from wydy.settings import PROJECT_ROOT

path = os.path.join(PROJECT_ROOT,'random')
fileHandle = open(path,'w')

def gen(start,end,bal):
    for n in range(start,end):
        x = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        card=Card(number=n,password=x,balance=bal)
        fileHandle.write(str(n) + '\t\t' + x +'\n')
        card.save()

def GenPassword(sender,**kwargs):
    gen(0,100,0)
    gen(100,300,0)
    gen(300,450,0)
    gen(450,480,0)
    gen(480,500,0)
    fileHandle.close()


def InitialResvNumber(sender,**kwargs):
    number=ResvNumber()
    number.save()
    
post_syncdb.connect(GenPassword,sender=userapp)
post_syncdb.connect(InitialResvNumber,sender=userapp)


'''
def GenPassword(length=8, chars=string.letters+string.digits):
    while True:
        yield ''.join([choice(chars) for i in range(length)])

def pass_gen(sender, **kwargs):
    line1=list()
    for i in xrange(500):
        for item in GenPassword():
            line1.append(item)
    line2=list(set(line1))
    n=0
    for str in line2:
        p=Card(number=n,password=str)
        p.save()
        n+=1;
'''
