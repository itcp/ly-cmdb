from __future__ import absolute_import

from django.urls import path

from .. import views

app_name = 'onlineconfig'

urlpatterns = [
    # nginx
    #path('',views.index),
    path('nginx/', views.NginxIndexVies.as_view(), name='nginx'),
    #path('nginx/', views.nginx_index, name='nginx')
    
    path('nginx/create_conf', views.create_conf, name='create_conf')

]