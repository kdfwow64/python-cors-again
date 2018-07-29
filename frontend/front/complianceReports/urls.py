from django.conf.urls import url

from complianceReports import views

urlpatterns =[
  url(r'^$', views.complianceReportsList, name='complianceReportsList'),
  url(r'complianceReportView/$', views.complianceReportView, name='complianceReportView'),
  url(r'complianceExecutionList/$', views.complianceExecutionList, name='complianceExecutionList'),
  url(r'complianceReportsCreate/$', views.complianceReportsCreate, name='complianceReportsCreate'),
#   url(r'^newReport$', views.newComplianceRepport, name='newComplianceRepport'),

]