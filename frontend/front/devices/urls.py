from django.conf.urls import url

from devices import views

urlpatterns =[
  url(r'^$', views.Device, name='Device'),
  url(r'devicereport/$', views.DeviceReport, name='DeviceReport'),
]