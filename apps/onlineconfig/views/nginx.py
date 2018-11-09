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
import os,sys

from common.utils import get_logger

class NginxIndexVies(TemplateView):
    template_name = "onlineconfig/confnginx.html"


@csrf_protect
def create_conf(request):
    
    hostip = '192.168.181.133'
    conf_dir = '/usr/local/src/'
    if request.is_ajax():
        server_name = request.GET['server_name']
        root_dir = request.GET['root_dir']

        os.system('ssh root@' + hostip + ' "cp ' + conf_dir + 'server.conf ' + conf_dir + server_name + '.conf"')

        update_rootdir = "'sed -i \"s#/home/wwwroot/dist;#/home/wwwroot/" + root_dir + ";#g\" " + conf_dir + server_name +".conf'"
        update_servername = "'sed -i \"s#server_name benz.huihuang200.com;#server_name " + server_name + ";#g\" " + conf_dir+ server_name +".conf'"
        update_log = "'sed -i \"s#/home/wwwlogs/benz.huihuang200.com.log#/home/wwwlogs/" + server_name + ".log#g\" " + conf_dir + server_name +".conf'"
        update_errorlog = "'sed -i \"s#/home/wwwlogs/benz.huihuang200.com.error.log#/home/wwwlogs/" + server_name + ".error.log#g\" " + conf_dir + server_name +".conf'"

        os.system('ssh root@' + hostip + ' ' + update_rootdir)
        os.system('ssh root@' + hostip + ' ' + update_servername)
        os.system('ssh root@' + hostip + ' ' + update_log)
        os.system('ssh root@' + hostip + ' ' + update_errorlog)
        os.system('nginx -s reload')

        receipt = json.dumps({"status": 2, "info": request.GET})
    else:
        receipt = json.dumps(0)
    
    return HttpResponse(receipt)

