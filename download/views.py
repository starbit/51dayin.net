# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render_to_response, HttpResponse,get_object_or_404
from datetime import date
from fileupload.models import Order
import os
from wydy.settings import PROJECT_ROOT


def download_filelist(request, s):
    day = date.today()
    string = hex(int(day.strftime('%Y%m%d')))[2:]
    if s == string:
        empty = Order.objects.filter(requirement = None)
        for e in empty:
            e.delete()
        ord = Order.objects.filter(download = False)
        if ord:
            path = os.path.join(PROJECT_ROOT,'media','file_list.txt')
            fileHandle = open(path,'w')
            content = ""
            for o in ord:
                content += "%s "%o.slug
            fileHandle.write(content)
            response = HttpResponse(content,content_type='application/txt')
            response['Content-Disposition'] = 'attachment; filename=file_list.txt'#改name
            response['Content-Length'] = fileHandle.tell()

            fileHandle.close()
            return response
 

def download_zipfile(request, ord_slug):
    import tempfile, zipfile
    from django.core.servers.basehttp import FileWrapper
    
    ord = Order.objects.get(slug=ord_slug)
    ord.download = True
    ord.save()
    temp = tempfile.TemporaryFile()
    archive = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED)
    src = os.path.join(PROJECT_ROOT, 'media','files',ord.slug)
    files = os.listdir(src)
    for filename in files:
        archive.write(src+'/'+filename, filename)
    archive.close()
    wrapper = FileWrapper(temp)
    response = HttpResponse(wrapper, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=file.zip'#改name
    response['Content-Length'] = temp.tell()
    temp.seek(0)
    return response
