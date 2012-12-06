# -*- coding: utf-8 -*-

from fileupload.models import File
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render_to_response, HttpResponse,get_object_or_404
from forms import *
from django.template.response import TemplateResponse
from user.models import ResvNumber
from datetime import datetime,date,timedelta
import os
from wydy.settings import PROJECT_ROOT
from django.views.decorators.csrf import csrf_exempt


def gen():
    number = ResvNumber.objects.get(id=1)
    if number.resv_number == 256:
        number.resv_number = 0
        number.save()
    number.resv_number += 1
    s = hex(number.resv_number)
    s1 = s[2:]
    if len(s1) < 2:
        s1 = "0" + s1
    number.save()
    return s1

@csrf_exempt
def upload_handle(request, user_id, ord_id, req_id):
    """
    receive file 
    """
    if  request.FILES:

        req = Requirement.objects.get(id = req_id)
        ord = Order.objects.get(id = ord_id)
        for file in request.FILES.getlist('Filedata'):
            print 'file  name',file.name
            f = File(slug = ord.slug)
            f.requirement_id = req_id
            f.file = file
            f.save()
            req.file.add(f)
        
            #保存相应的打印要求文件
            import codecs
            path = os.path.join(PROJECT_ROOT,'media','files',ord.slug,"REQUEST%s.txt"%file.name)
            fileHandle = codecs.open(path,encoding='utf-8',mode='w')
            content = u"纸张:%s\n页面范围:%s\n%s\n每页%s版\n%d份\n备注:%s\n"%(req.paper,req.range,req.singleordouble,req.style,req.copies,req.note)
            fileHandle.write(content)
            fileHandle.close()

        return HttpResponse('1')



@csrf_exempt
@login_required
def upload(request, user_id, ord_id, req_id):
    req_id = int(req_id)
    ord_id = int(ord_id)
    req = Requirement.objects.get(id = req_id)
    ord = Order.objects.get(id = ord_id)
    #print (req.file.count())
    if (int(request.user.id) == int(user_id)) and (req.file.count() == 0):
        if request.method == 'GET':
            form = FileForm()
        return TemplateResponse(request,"fileupload/file_form.html",{'active':'file','form':form,'warning':u'','user_id':user_id,'ord_id':ord_id,'req_id':req_id})
    else:
        return TemplateResponse(request,"404.html")

@login_required
def requirement(request, user_id, ord_id):
    if request.method == 'POST':
        form = RequirementForm(request.POST)
        if form.is_valid():
            req = form.save()
            req.order_id = int(ord_id)
            req.save()
            ord = Order.objects.get(id = int(ord_id))
            ord.requirement.add(req)
            return redirect('/file/upload/%d/%d/%d/'%(int(request.user.id),int(ord.id),req.id))
    else:
        form = RequirementForm()
    return TemplateResponse(request,"requirement.html",{'active':'file','form':form,'ord_id':ord_id,'user_id':user_id})

@login_required
def order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            ord = form.save()
            ord.resv_number = gen()
            ord.user = request.user.username
            d = date(ord.resv_date.year,ord.resv_date.month,ord.resv_date.day)
            if ord.day == "1":
                d = d + timedelta(1)
            slug = "%s-%s-%s_%s_%s"%(str(d),ord.hour,ord.minute,ord.resv_number,ord.user)
            ord.slug = slug
            print slug
            ord.save()
            return redirect('/file/requirement/%d/%d/'%(int(request.user.id),int(ord.id)))
    else:
        form = OrderForm()
    return TemplateResponse(request,"order.html",{'active':'file','form':form})

@login_required
def cancel(request, user_id, ord_id):
    if request.user.id == int(user_id):
        ord = Order.objects.get(id = int(ord_id))
        ord.delete()
        return redirect(request,'/file/')
    else:
        return TemplateResponse(request, '404.html')
    
@login_required
def add(request,user_id, ord_id):
    return TemplateResponse(request,"fileupload/add.html",{'active':'file','user_id':str(user_id),'ord_id':str(ord_id)})

@login_required
def success(request,ord_id):
    resv_number = Order.objects.get(id = ord_id).resv_number
    return TemplateResponse(request,"success.html",{'active':'file','resv_number':resv_number})
