# -*- coding: utf-8 -*-

from django import forms
from django.forms.util import ErrorList
from django.forms import ModelForm
from models import Requirement, Order

#预约打印的表单

class RequirementForm(ModelForm):
    class Meta:
        model = Requirement
        exclude = ('file','order_id')
    copies = forms.IntegerField(error_messages = {'required': u'忘记写份数了哦','max_value':u'最多50份啦','min_value':u'至少1份诶'},min_value=1, max_value = 50)
    def clean(self):
        note = self.cleaned_data['note']
        print note
        range = self.cleaned_data['range']
        #print range
        if (range == u"自定义")and(note == " "):
            self._errors['note'] = ErrorList([u'请填写自定义页码范围~'])
        
        return self.cleaned_data
class FileForm(forms.Form):
    file = forms.FileField(error_messages = {'required':u'请添加文件'})


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ('printhouse','day','hour','minute',)