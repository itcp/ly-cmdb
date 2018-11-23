# ~*~ coding: utf-8 ~*~
import uuid

from django.core.cache import cache
from django.contrib.auth import logout
from django.utils.translation import ugettext as _

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_bulk import BulkModelViewSet
from rest_framework import serializers

from orgs.utils import current_org
from common.permissions import IsOrgAdmin, IsCurrentUserOrReadOnly, IsOrgAdminOrAppUser
from common.mixins import IDInFilterMixin
from common.utils import get_logger

from ops.ansible.runner import AdHocRunner, CommandRunner
from ops.ansible.inventory import BaseInventory
from rest_framework.views import APIView


logger = get_logger(__name__)
__all__ = [
    'GetOssViewSet',
]

class GetOssViewSet(APIView):
    def get(self, request, format=None):
    
        return Response({'status': 'ok'})

class SetOssAccessViewSet(APIView):
    def get(self, request, format=None):
        #auth = oss2.Auth('LTAI0iNRHjVkT7wv', 'pvSfPWuzBr4yw7tYcglI9IuKgBzBXT')
        bucket = oss2.Bucket(auth, 'http://oss-cn-hongkong.aliyuncs.com', request.data['bucketname'])
        if request.data['status'] == 'on':
            bucket.put_bucket_acl('public-read')
        elif request.data['status'] == 'off':
            bucket.put_bucket_acl('private')
        
