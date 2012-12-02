from django.conf.urls.defaults import *
from views import *


urlpatterns = patterns('download.views',

    url(r'^(?P<ord_slug>\S+)/$', 'download_zipfile',name='download_zipfile'),
    url(r'^filelist/(?P<s>\w+)$', 'download_filelist',name='download_filelist'),


)

