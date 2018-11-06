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
import json
from django.views.decorators.csrf import csrf_protect

from common.utils import get_logger

#__all__ = ['confnginx']
#logger = get_logger(__name__)

class NginxIndexVies(TemplateView):

        #ctx['server_name'] = request.POST['server_name']
        #ctx['server_name'] = request.POST['server_name']
        #ctx['server_name'] = request.POST['server_name']

    template_name = "onlineconfig/confnginx.html"
    #template_name = "onlineconfig/conf_nginx.html"
"""

def nginx_index(request):
    return HttpResponse("<p>lh</p>")
    #return render(request, 'onlineconfig/confnginx.htm')
"""
@csrf_protect
def create_conf(request):
    
    #if request.POST:
    #    ctx['server_name'] = request.POST['server_name']
    
    #receipt = json.dumps({"status": 1, "servername":request.POST})
    print(3)
    if request.is_ajax():
        receipt = json.dumps(request.GET)
    else:
        receipt = json.dumps(1)
    return HttpResponse(receipt)

