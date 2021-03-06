# coding:utf-8
from django.urls import path
from rest_framework_nested import routers
# from rest_framework.routers import DefaultRouter
from rest_framework_bulk.routes import BulkRouter

from .. import api

app_name = 'onlineconfig'

urlpatterns = [
    path('nginx-conf/', api.NginxConfigViewSet.as_view(), name='nginx-conf-list'),
]
