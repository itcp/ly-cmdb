# coding:utf-8
from django.urls import path
from rest_framework_nested import routers
# from rest_framework.routers import DefaultRouter
from rest_framework_bulk.routes import BulkRouter

from .. import api

app_name = 'onlineconfig'

#router = BulkRouter()
#router.register(r'onlineconfig', api.AssetViewSet, 'onlineconfig')


#cmd_filter_router = routers.NestedDefaultRouter(router, r'cmd-filter', lookup='filter')
#cmd_filter_router.register(r'rules', api.CommandFilterRuleViewSet, 'cmd-filter-rule')


urlpatterns = [
    path('nginx-conf/', api.NginxConfigViewSet.as_view(), name='nginx-conf-list'),
    #path('system-user/<uuid:pk>/auth-info/',
    #     api.SystemUserAuthInfoApi.as_view(), name='system-user-auth-info'),

]


