from django.conf.urls import url

from dashboards import views

urlpatterns =[
  url(r'^$', views.Dashboard, name='Dashboards'),
  url(r'^dashboardElements$', views.DashboardElement, name='DashboardElements'),
  #url(r'^divbloc$', views.Getit, name='Getit'),
  #url(r'^delete$', views.delete, name='delete'),
  

]