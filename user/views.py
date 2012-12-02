# -*- coding: utf-8 -*-

from django import forms
from django.template import RequestContext,Template, Context
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate,logout
from .forms import JoinForm, ResetPasswordForm, ChangePasswordForm
from django.contrib.auth.forms import PasswordResetForm
from django.shortcuts import redirect, render_to_response, HttpResponse,get_object_or_404
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.transaction import commit_on_success
from wydy.settings import DEFAULT_FROM_EMAIL

import urllib2

from models import *
from forms import *

@commit_on_success
def join(request):
    if request.method == 'POST':
        form = JoinForm(request.POST)
        if form.is_valid():
            cardNumber = form.cleaned_data['cardNumber']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            phone = form.cleaned_data['phone']
            card = Card.objects.get(number=cardNumber)
            balance = card.balance
            user=User.objects.create_user(username=username, email=email, password=password)
            userprofile=user.get_profile()
            userprofile.balance=5
            userprofile.points=0
            userprofile.phone=phone
            userprofile.save()
            card.delete()
            user = authenticate(username=username, password=password)
            login(request, user)
            
            return redirect('/file/')
    else:
        form = JoinForm()
    
    return TemplateResponse(request, 'join.html', {'form': form})	

def about(request):
	return TemplateResponse(request,"about.html")
'''
def browser_support(request):
    return TemplateResponse(request,"browser_support.html")
'''
def major_id(request):
    return TemplateResponse(request,"major_id.html")
def others(request):
    return TemplateResponse(request,"others.html")

def home(request):
    if request.user.is_authenticated():
        return redirect('/file/')
    else:
        return TemplateResponse(request,"home.html")
@login_required
def tasklist(request):
	return TemplateResponse(request,"user/tasklist.html",{'active':'tasklist'})
'''
def hot(request):
	return TemplateResponse(request,"hot.html")
'''

@login_required
def profile(request):
    #balance = profile.balance
    #points = profile.points
    return TemplateResponse(request,"user/profile.html",{'active1':'profile','active':'settings'})
@csrf_exempt
@login_required
def settings(request, item):
    #profile = request.user.get_profile()
    
    if item == "profile":
        return profile(request)
    elif item == "psw":
        return _set_psw(request)
    else:
        raise Http404("no setting")

def reset_psw(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(domain_override=request.get_host(), from_email=DEFAULT_FROM_EMAIL, email_template_name="user/password_reset_email.html")
            return render_to_response('user/reset_psw_sended.html', {})
        else:
            
            return TemplateResponse(request, 'user/reset_psw.html', {'form': form})
    form = PasswordResetForm()
    return TemplateResponse(request, 'user/reset_psw.html', {'form': form})


def reset_psw_confirm(request, uid, token):
    from django.utils.http import base36_to_int
    user = User.objects.get(pk = base36_to_int(uid))
    
    if request.method == 'POST':
        form = ResetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            return render_to_response('user/reset_psw_done.html', {})
        else:
            return TemplateResponse(request, 'user/reset_psw_confirm.html', {'form': form})
    form = ResetPasswordForm(user)
    return TemplateResponse(request, 'user/reset_psw_confirm.html', {'form': form})

def _set_psw(request):
    if request.method == 'POST':
        form = ChangePasswordForm(user = request.user, data = request.POST)
        if form.is_valid():
            form.save()
            return render_to_response('user/change_psw_done.html', {})
        else:
            return TemplateResponse(request, 'user/setting_psw.html', {'form': form, 'active':'psw'})
    form = ChangePasswordForm(user = request.user)
    return TemplateResponse(request, 'user/setting_psw.html', {'form': form, 'active1':'psw','active':'settings'})





def create_user(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = UserForm()

    t = get_template('admin/create_user.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))



def list_user(request):
  
    list_items = User.objects.all()
    paginator = Paginator(list_items ,10)


    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        list_items = paginator.page(page)
    except :
        list_items = paginator.page(paginator.num_pages)

    t = get_template('admin/list_user.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))

@login_required
def contact(request):
    if request.method=='POST':
        form=ContactForm(request.POST)
        if form.is_valid():
            topic = form.cleaned_data['topic']
            message = form.cleaned_data['message']
            sender = form.cleaned_data.get('sender','fiftycent@people.cn')
            send_mail(
                'feedback from user, topic: %s sender:%s'%(topic,sender),
                message,'marvin@51dayin.net',['marvin@51dayin.net']
            )
            return redirect('/thanks/')
    else:
        form=ContactForm()
    return TemplateResponse(request,'contact.html',{'form':form,'active':'contact'})

def thanks(request):
    return TemplateResponse(request,'thanks.html')

def view_user(request, id):
    user_instance = User.objects.get(id = id)

    t=get_template('admin/view_user.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))

def edit_user(request, id):

    user_instance = User.objects.get(id=id)

    form = UserForm(request.POST or None, instance = user_instance)

    if form.is_valid():
        form.save()

    t=get_template('admin/edit_user.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))
def server_error(request, template_name='500.html'):
    r = render_to_response(template_name,
                           context_instance = RequestContext(request)
                           )
    r.status_code = 500
    return r

def server_error_404(request, template_name='404.html'):
    r =  render_to_response(template_name,
                            context_instance = RequestContext(request)
                            )
    r.status_code = 404
    return r
