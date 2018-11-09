from __future__ import absolute_import

from django.urls import path

from .. import views

app_name = 'architecture'

urlpatterns = [

    path('keepnet/', views.keepnet, name='keepnet'),
    path('keepnet/get_keep/', views.get_keep, name='get_keep'),
    
]