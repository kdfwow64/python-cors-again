
from django.conf.urls import url

from reports import views

urlpatterns =[
  url(r'^$', views.JobReportList, name='ReportList'),
  url(r'^tasks/$', views.TaskReportList, name='TaskViews'),
  url(r'^export_result/(?P<job_id>\w+)/$', views.exportCSVResult, name='export_csv_result'),
]