
from django.conf.urls import url

from mop import views
 
urlpatterns =[
  url(r'^$', views.workflowList, name='workflowList'),
  url(r'^workflow-edit/$', views.workflowEdit, name='workflowViews'),
  url(r'^workflow-delete/$', views.workflowDelete, name='workflowViews'),

]