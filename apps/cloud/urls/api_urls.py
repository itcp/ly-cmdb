from django.urls import path
from rest_framework_nested import routers
# from rest_framework.routers import DefaultRouter
from rest_framework_bulk.routes import BulkRouter

from .. import api

app_name = 'cloud'

urlpatterns = [
    path('aliyun-getoss/', api.aliyun.GetOssViewSet.as_view(), name='aliyun-getoss'),
]
