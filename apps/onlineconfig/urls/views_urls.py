from __future__ import absolute_import

from django.urls import path

from .. import views

app_name = 'onlineconfig'

urlpatterns = [
    # nginx
    #path('',views.index),
    path('nginx/', views.NginxIndexVies.as_view()),

]