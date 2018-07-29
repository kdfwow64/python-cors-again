"""front URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from jobs import views as jobs_views
from devices import views as devices_views
from dashboards import views as dashboards_views
from mop import views as workflow_views
from reports import views as reports_views
from user import views as user_views
from notifications import views as notifications_views
from workflowReports import views as workflowReports_views
from complianceReports import views as complianceReports_views


urlpatterns = [
    url(r'^$', user_views.Login, name='login'),
    url(r'^logout$', user_views.Logout, name='logout'),
    url(r'^notifications$', notifications_views.Notification, name='Notification'),
    url(r'^triggers$', notifications_views.Trigger, name='Trigger'),
    url(r'^index$', devices_views.Index, name='Index'),
    url(r'^admin/', admin.site.urls),
    url(r'^jobs/', include('jobs.urls', namespace='jobs')),
    url(r'^devices/', include('devices.urls', namespace='devices')),
    url(r'^dashboards/', include('dashboards.urls', namespace='dashboards')),
    url(r'^workflow/', include('mop.urls', namespace='workflow')),
    url(r'^reports/', include('reports.urls', namespace='reports')),
    url(r'^user/', include('user.urls', namespace='user')),
    url(r'^workflowReports/', include('workflowReports.urls', namespace='workflowReports')),
    url(r'^complianceReports/', include('complianceReports.urls', namespace='complianceReports')),


]


