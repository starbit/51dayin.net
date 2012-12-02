# -*- coding: utf-8 -*-

from django.db import models
import os
from datetime import datetime
def get_file_path(instance, filename):
        return os.path.join('files', str(instance.slug), filename)

class File(models.Model):

    file = models.FileField(upload_to=get_file_path)
    slug = models.SlugField(max_length=50, blank=True,null=True)
    requirement_id = models.IntegerField(blank=True,null=True)
    
    
    def __unicode__(self):
        return self.file.name


PRINTHOUSE=(
            (u'经C','经C泰和书屋旁'),
            #   (u'男孩女孩','男孩女孩超市内'),
            )
PAPER=(
       ('A4','A4'),
       ('B5','B5'),
       )

RANGE=(
       (u'全部','全部'),
       (u'自定义','自定义'),
       )

SINGLEORDOUBLE=(
                (u'双面','双面'),
                (u'单面','单面'),
                )
STYLE=(
       ('1','每页1版(适合.doc/.pdf)'),
       ('2','每页2版'),
       ('4','每页4版'),
       ('6','每页6版'),
       ('8','每页8版(适合.ppt)'),
       ('9','每页9版(适合.ppt)'),
       )
HOUR=(
      ('07','7'),
      ('08','8'),
      ('09','9'),
      ('10','10'),
      ('11','11'),
      ('12','12'),
      ('13','13'),
      ('14','14'),
      ('15','15'),
      ('16','16'),
      ('17','17'),
      ('18','18'),
      ('19','19'),
      ('20','20'),
      ('21','21'),
      ('22','22'),
      )
MINUTE=(
        ('00','00'),
        ('05','05'),
        ('10','10'),
        ('15','15'),
        ('20','20'),
        ('25','25'),
        ('30','30'),
        ('35','35'),
        ('40','40'),
        ('45','45'),
        ('50','50'),
        ('55','55'),
        
        )
DAY=(
     ('0','当日'),
     ('1','次日'),
     )

class Requirement(models.Model):
    paper = models.CharField(max_length=20,choices=PAPER)
    range = models.CharField(max_length=10,choices=RANGE)
    singleordouble = models.CharField(max_length=10,choices=SINGLEORDOUBLE)
    style =models.CharField(max_length=30,choices=STYLE)
    copies = models.IntegerField()
    note = models.CharField(max_length=100,blank=True)

    file = models.ManyToManyField(File,blank=True,null=True)
    #slug = models.SlugField(max_length=50, blank=True)
    order_id = models.IntegerField(blank=True,null=True)
    def __unicode__(self):
        return "%s %s %s %s %d %s"%(self.paper,self.range,self.singleordouble,self.style,self.copies,self.note)

class Order(models.Model):
    requirement = models.ManyToManyField(Requirement,blank=True,null=True)
    resv_date = models.DateTimeField(default=datetime.now, blank=True)
    printhouse = models.CharField(max_length=50,choices=PRINTHOUSE)
    resv_number = models.CharField(max_length=2,blank=True)
    day = models.CharField(max_length=2,choices=DAY)
    hour = models.CharField(max_length=3,choices=HOUR)
    minute= models.CharField(max_length=3,choices=MINUTE)
    user = models.CharField(max_length=10,blank=True)
    download = models.BooleanField(default=False,blank=True)
    slug = models.SlugField(max_length=50, blank=True)
    
    def __unicode__(self):
        return self.slug

#draw = models.BooleanField(default=False)
#cost = models.DecimalField(max_digits=5,decimal_places=2,default=0)
#finish = models.BooleanField(default=False)


