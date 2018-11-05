# ~*~ coding: utf-8 ~*~

from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.http import HttpResponse

from common.utils import get_logger

#__all__ = ['confnginx']
#logger = get_logger(__name__)

class NginxIndexVies(TemplateView):
    template_name = "onlineconfig/conf_nginx.html"

