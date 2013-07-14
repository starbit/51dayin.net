# Create your views here.
from django.shortcuts import redirect
from django.template.response import TemplateResponse

def home(request):
    if request.user.is_authenticated():
        return redirect('/file/')
    else:
        return TemplateResponse(request,"home/index.html")

def about(request):
    return TemplateResponse(request,"home/about.html")

def major_id(request):
    return TemplateResponse(request,"home/major_id.html")

def thanks(request):
    return TemplateResponse(request,'home/thanks.html')