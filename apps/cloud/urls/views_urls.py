from __future__ import absolute_import

from django.urls import path

from .. import views

app_name = 'cloud'

urlpatterns = [
    path('aliyun-syncoss/', views.aliyun.oss.SyncOssView, name='aliyun-syncoss'),
]
