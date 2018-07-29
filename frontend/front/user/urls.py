from django.conf.urls import url

from user import views

urlpatterns =[
  url(r'^role/create$', views.RoleCreate, name='role_create'),
  url(r'^role/delete/(?P<obj_id>\w+)/$', views.RoleDelete, name='role_delete'),
  url(r'^role/edit/(?P<obj_id>\w+)/$', views.RoleEdit, name='role_edit'),
  url(r'^role$', views.Role, name='role'),

  url(r'^user_group/create$', views.UserGroupCreate, name='user_group_create'),
  url(r'^user_group/delete/(?P<obj_id>\w+)/$', views.UserGroupDelete, name='user_group_delete'),
  url(r'^user_group/edit/(?P<obj_id>\w+)/$', views.UserGroupEdit, name='user_group_edit'),
  url(r'^user_group$', views.UserGroup, name='user_group'),

  url(r'^create$', views.UserCreate, name='user_create'),
  url(r'^delete/(?P<obj_id>\w+)/$', views.UserDelete, name='user_delete'),
  url(r'^edit/(?P<obj_id>\w+)/$', views.UserEdit, name='user_edit'),
  url(r'^$', views.User, name='user'),

]