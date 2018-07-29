
from django.conf.urls import url

from workflowReports import views

urlpatterns =[
  url(r'^$', views.workflowReportList, name='workflowReportList'),
  url(r'^job/$', views.JobReportList, name='jobViews'),

]