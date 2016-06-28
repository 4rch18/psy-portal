from django.conf.urls import url

from . import views

urlpatterns = (
    url(r'^$', views.index, name='index'),
    url(r'^home/$', views.home, name='home'),
    url(r'^logout/(?P<userID>[0-9]+)/$', views.logout, name='logout'),
    url(r'^addHours/(?P<adminID>[0-9]+)/$', views.addHours, name='addHOurs'),
    url(r'^chat/(?P<clientID>[0-9]+)/(?P<adminID>[0-9]+)/$', views.chat, name='chat'),
    url(r'^admin_chat/(?P<clientID>[0-9]+)/(?P<adminID>[0-9]+)/$', views.admin_chat, name='admin_chat'),
    url(r'^book/(?P<clientID>[0-9]+)/(?P<adminID>[0-9]+)/$', views.book, name='book'),
    url(r'^deleteHours/(?P<adminID>[0-9]+)/(?P<officeHoursID>[0-9]+)/$', views.deleteHours, name='deleteHours'),
)