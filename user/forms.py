# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.forms.util import ErrorList
from django.forms import ModelForm
from models import Card

class LoginForm(AuthenticationForm):
    username = forms.CharField(error_messages = {'required': u'用户名不能为空诶童鞋～'},max_length = 10,min_length=8)
    password = forms.CharField(error_messages = {'required': u'密码不能为空诶少年～'},max_length = 16,min_length = 8,widget = forms.PasswordInput)
    def clean(self):
            username = self.cleaned_data.get('username')
            password = self.cleaned_data.get('password')
            if username and password:
                self.user_cache = authenticate(username=username, password=password)
                if self.user_cache is None:
                        raise forms.ValidationError("密码错误啦~")
            self.check_for_test_cookie()
            return self.cleaned_data




class JoinForm(forms.Form):
	cardNumber = forms.IntegerField(error_messages = {'required': u'请填写卡号',})
	cardPassword = forms.CharField(error_messages = {'required': u'请填写卡密'})
	username = forms.CharField(error_messages = {'required': u'请填写用户名','max_length':u'研究生是10位哦','min_length':u'本科生8位哦'},min_length=8, max_length = 10)
	password = forms.CharField(error_messages = {'required': u'密码不能为空哦','max_length':u'至少8位啦','min_length':u'最多16位呢'},widget = forms.PasswordInput,max_length = 16,min_length=8)
	confirm_password = forms.CharField(error_messages = {'required': u'确认密码不能为空哦','max_length':u'至少8位啦','min_length':u'最多16位呢'},widget = forms.PasswordInput,max_length=16,min_length=8)
	email = forms.EmailField(error_messages = {'required': u'请填写邮箱'})
	phone = forms.CharField(error_messages = {'required': u'怎么能不写呢','max_length':u'给记错自己手机号码的人跪了..','min_length':u'给记错自己手机号码的人跪了..'},widget = forms.TextInput(),max_length = 11,min_length=11)
    
        def clean_cardNumber(self):
            cardNumber = self.cleaned_data['cardNumber']
            exists = Card.objects.filter(number = cardNumber).count() > 0
            if not exists:
                raise forms.ValidationError(u'卡号不存在或已被使用了哦，请重新输入或购买~')
            return cardNumber
        def clean_cardPassword(self):
            cardPassword = self.cleaned_data['cardPassword']
            exists = Card.objects.filter(password=cardPassword).count() > 0
            if not exists:
                raise forms.ValidationError(u'卡密输入错误~')
            return cardPassword
        def clean_phone(self):
            phone = self.cleaned_data['phone']
            if phone[0]!='1':
                raise forms.ValidationError(u'难道墙内的手机不是1开头么少年..')
            if not phone.isdigit():
                raise forms.ValidationError(u'请用阿拉伯数字哦亲~')
        
    
        def clean_username(self):
            username = self.cleaned_data['username']
            exists = User.objects.filter(username = username).count() > 0
            if exists:
                raise forms.ValidationError(u'该用户名已被使用了呢，请重新输入')
            if not username.isdigit():
                raise forms.ValidationError(u'学号是数字哦')
            return username
    
        def clean(self):
            if ('confirm_password' in self.cleaned_data) and ('password' in self.cleaned_data):
                if (self.cleaned_data['confirm_password'] != self.cleaned_data['password']):
                    self._errors["confirm_password"] = ErrorList([u'密码与确认密码不匹配耶～'])
                    del self.cleaned_data['password']
                    del self.cleaned_data['confirm_password']
            if ('cardPassword' in self.cleaned_data)and ('cardNumber' in self.cleaned_data):
                cardPassword = self.cleaned_data['cardPassword']
                cardNumber = self.cleaned_data['cardNumber']
                card = Card.objects.get(number=cardNumber)
                if card.password != cardPassword:
                    self._errors["cardPassword"] = ErrorList([u'卡密与卡号不对应呢，请重新输入或购买~'])
                    del self.cleaned_data['cardNumber']
                    del self.cleaned_data['cardPassword']
                
            return self.cleaned_data
    
        def clean_email(self):
            email = self.cleaned_data['email']
            exists = User.objects.filter(email = email).count() > 0
            if exists:
                raise forms.ValidationError(u'邮箱已经被使用了呢，请更换邮箱')
            return email



class GetPasswordForm(forms.Form):
    email = forms.EmailField(max_length = 75, widget = forms.TextInput())
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email = email).count() != 1:
            raise forms.ValidationError("这个邮箱木有对应的帐号诶～")
        return email

class ChangePasswordForm(PasswordChangeForm):
    old_password  = forms.CharField(label="原密码", widget=forms.PasswordInput, error_messages = {'required': u'新密码不能为空哦', 'min_length':u'至少8个字符啦', 'max_length':u'最多16个字符啦'}, min_length = 8, max_length = 16)
    new_password1 = forms.CharField(label="新密码", widget=forms.PasswordInput, error_messages = {'required': u'新密码不能为空哦', 'min_length':u'至少8个字符啦', 'max_length':u'最多16个字符啦'}, min_length = 8, max_length = 16)
    new_password2 = forms.CharField(label="新密码确认", widget=forms.PasswordInput, error_messages = {'required': u'新密码不能为空哦', 'min_length':u'至少8个字符啦', 'max_length':u'最多16个字符啦'}, min_length = 8, max_length = 16)


class ResetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label="新密码", widget=forms.PasswordInput, error_messages = {'required': u'新密码不能为空哦', 'min_length':u'至少8个字符啦', 'max_length':u'最多16个字符啦'}, min_length = 8, max_length = 16)
    new_password2 = forms.CharField(label="新密码确认", widget=forms.PasswordInput, error_messages = {'required': u'新密码不能为空哦', 'min_length':u'至少8个字符啦', 'max_length':u'最多16个字符啦'}, min_length = 8, max_length = 16)

TOPIC=(
    ('ux','用户体验'),
    ('bug','有bug!'),
    ('suggestion','建议'),
)

class ContactForm(forms.Form):
    topic = forms.ChoiceField(choices=TOPIC,label="主题")
    message = forms.CharField(widget=forms.Textarea(),label="内容",error_messages = {'required': u'内容为空？元芳，这不科学。'})
    sender = forms.EmailField(required=False,label="联系邮箱")
    def clean_message(self):
        message = self.cleaned_data.get('message','')
        if len(message) < 8:
            raise forms.ValidationError("元芳多说一点别那么小气啦!")
        return message
