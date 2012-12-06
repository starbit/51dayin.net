from django.conf.urls.defaults import *
from views import *


urlpatterns = patterns('fileupload.views',
    url(r'^uploadhandle/(?P<user_id>\d+)/(?P<ord_id>\d+)/(?P<req_id>\d+)/$', 'upload_handle',name='upload-handle'),
    url(r'^upload/(?P<user_id>\d+)/(?P<ord_id>\d+)/(?P<req_id>\d+)/$', 'upload',name='upload-new'),

    url(r'^success/(?P<ord_id>\d+)/$', 'success',name='success'),

    url(r'^$', 'order',name='order'),
    url(r'^add/(?P<user_id>\d+)/(?P<ord_id>\d+)/$', 'add',name='add'),
    url(r'^cancel/(?P<user_id>\d+)/(?P<ord_id>\d+)/$', 'cancel',name='cancel'),

    url(r'^requirement/(?P<user_id>\d+)/(?P<ord_id>\d+)/$', 'requirement',name='requirement'),


)

