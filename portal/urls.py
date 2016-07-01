from django.conf.urls import url

from . import views

urlpatterns = (
    url(r'^$', views.index, name='index'),
    url(r'^home/$', views.home, name='home'),
    url(r'^home/(?P<clientID_from_url>[0-9]+)/$', views.home, name='home'),
    url(r'^addHours/(?P<adminID>[0-9]+)/$', views.addHours, name='addHOurs'),
    url(r'^chat/(?P<clientID>[0-9]+)/(?P<adminID>[0-9]+)/$', views.chat, name='chat'),
    url(r'^call/(?P<clientID>[0-9]+)/(?P<adminID>[0-9]+)/$', views.call, name='call'),
    url(r'^admin_call/(?P<clientID>[0-9]+)/(?P<adminID>[0-9]+)/$', views.admin_call, name='admin_call'),
    url(r'^admin_chat/(?P<clientID>[0-9]+)/(?P<adminID>[0-9]+)/$', views.admin_chat, name='admin_chat'),
    url(r'^book/(?P<clientID>[0-9]+)/(?P<adminID>[0-9]+)/$', views.book, name='book'),
    url(r'^deleteHours/(?P<adminID>[0-9]+)/(?P<officeHoursID>[0-9]+)/$', views.deleteHours, name='deleteHours'),
    url(r'^acceptRequest/(?P<clientID>[0-9]+)/(?P<adminID>[0-9]+)/$', views.acceptRequest, name='acceptRequest'),
    url(r'^getData/(?P<clientID>[0-9]+)/(?P<adminID>[0-9]+)/$', views.getData, name='getData'),
    url(r'^admin_getData/(?P<clientID>[0-9]+)/(?P<adminID>[0-9]+)/$', views.admin_getData, name='admin_getData'),
    url(r'^index/$', views.my_logout, name='logout'),


    url(r'^polling_home/(?P<clientID>[0-9]+)/$', views.polling_home, name='polling_home'),
    url(r'^admin_polling_home/(?P<adminID>[0-9]+)/$', views.admin_polling_home, name='admin_polling_home'),
)