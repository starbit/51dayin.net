from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from user.forms import LoginForm
from django.contrib.auth import views as auth_views
admin.autodiscover()

urlpatterns = patterns('')

urlpatterns += patterns('user.views',
    url(r'^join/$','join',name='join'),
    #url(r'^browser_support/$','browser_support',name='browser_support'),

    url(r'^major_id/$','major_id',name='major_id'),

    url(r'^contact/$','contact',name='contact'),
    url(r'^thanks/$','thanks',name='thanks'),

    url(r'^login/$', auth_views.login, {'template_name': 'login.html', 'authentication_form': LoginForm }, name = 'login'),

    url(r'^$','home',name='home'),
    url(r'^reset/$', 'reset_psw',name='reset_psw'),
    url(r'^reset/confirm/(?P<uid>\w+)/(?P<token>[-\w]+)/$', 'reset_psw_confirm', name = 'reset_psw_confirm'),
    #   url(r'^user/(?P<user_id>\d+)/$','user',name='user'),

    url(r'^user/tasklist/$','tasklist',name='tasklist'),

    url(r'^about/$','about',name='about'),
    #url(r'^hot/$','hot',name='hot'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'user.html','next_page':'/login/'}, name='logout'),
    url(r'^settings/(?P<item>\w+)/$', 'settings', name='settings'),

    (r'user/create/$', 'create_user'),
    (r'user/list/$', 'list_user' ),
    (r'user/edit/(?P<id>[^/]+)/$', 'edit_user'),
    (r'user/view/(?P<id>[^/]+)/$', 'view_user'),
)

urlpatterns += patterns('fileupload.views',
    url(r'^uploadhandle/(?P<user_id>\d+)/(?P<ord_id>\d+)/(?P<req_id>\d+)/$', 'upload_handle',name='upload-handle'),
    url(r'^upload/(?P<user_id>\d+)/(?P<ord_id>\d+)/(?P<req_id>\d+)/$', 'upload',name='upload-new'),

    url(r'^success/(?P<ord_id>\d+)/$', 'success',name='success'),

    url(r'^$', 'order',name='order'),
    url(r'^add/(?P<user_id>\d+)/(?P<ord_id>\d+)/$', 'add',name='add'),
    url(r'^cancel/(?P<user_id>\d+)/(?P<ord_id>\d+)/$', 'cancel',name='cancel'),

    url(r'^requirement/(?P<user_id>\d+)/(?P<ord_id>\d+)/$', 'requirement',name='requirement'),
)

urlpatterns += patterns('download.views',
    url(r'^(?P<ord_slug>\S+)/$', 'download_zipfile',name='download_zipfile'),
    url(r'^filelist/(?P<s>\w+)$', 'download_filelist',name='download_filelist'),
)

urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
'''
import os
urlpatterns += patterns('',
                        (r'^media/(.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.abspath(os.path.dirname(__file__)), 'media')}),
                        )
'''
