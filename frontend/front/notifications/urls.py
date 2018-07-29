from django.conf.urls import url

from notifications import views

urlpatterns =[
  url(r'^$', views.Notification, name='Notification'),
  url(r'^$', views.Trigger, name='Trigger'),
]


