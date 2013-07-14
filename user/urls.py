from django.conf.urls.defaults import *
from user.models import *
from user.views import *
from user.forms import LoginForm
from django.contrib.auth import views as auth_views

urlpatterns = patterns('user.views',
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
