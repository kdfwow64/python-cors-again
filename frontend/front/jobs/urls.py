from django.conf.urls import url

from jobs import views

urlpatterns =[
  url(r'^$', views.JobList, name='JobList'),
  url(r'^job-edit/$', views.JobEdit, name='JobViews'),
  url(r'^job-delete/$', views.JobDelete, name='JobViews'),
  url(r'^job-create/$', views.JobCreate, name='JobViews'),
]


