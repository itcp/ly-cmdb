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
    'NginxConfigViewSet', 'NginxUpdateConfApi'
]


host_data = [
    {
        "hostname": "nginx_1",
        "ip": "172.20.100.104",
        "port": 22,
        "username": "root",
            "groups": ["nginx"],
        #"password": "stu@python",
    }
]

example = 'example.com'

vhost_dir = '/usr/local/nginx/conf/vhost/'
master_nginx_conf = "/usr/local/nginx/conf/nginx.conf"
nginx_reload = '/usr/local/nginx/sbin/nginx -s reload'
www_dir = "/usr/local/nginx/html/"
old_www_dir = "/home/wwwroot/"

class NginxConfigViewSet(APIView):
    """
    返回所有nginx conf 配置文件名
    """

    def get(self, request, format=None):
        inventory = BaseInventory(host_data)
        runner = AdHocRunner(inventory)

        tasks = [
            {"action": {"module": "shell", "args": "ls "+vhost_dir}, "name": "lsvhost"},
           
        ]
        ret = runner.run(tasks, "all")
        
        return Response(ret.results_raw["ok"]["nginx_1"]["lsvhost"]["stdout_lines"])

    def post(self, request, format=None):
        dict_a = {}
        if request:
            post_a = request.data["domain"]

        inventory = BaseInventory(host_data)
        runner = AdHocRunner(inventory)

        tasks = [
            {"action": {"module": "copy", "args": \
            {"src": "/storage/" + example + "/", "dest": vhost_dir + request.data["domain"]}}, \
            "name": "copy" },

            {"action": {"module": "stat", \
            "args": {"path": vhost_dir + request.data["domain"] + "/lobby." + request.data["domain"] + ".conf"}}, \
            "name": "stat_lobby" },

            {"action": {"module": "shell", \
            "args": "for name in `ls " + vhost_dir + request.data["domain"] + "/*" + example + ".conf`;do mv $name ${name%." + example + ".conf}." + request.data["domain"] + ".conf;done"}, \
            "name": "rename_conf" },

            {"action": {"module": "shell", \
            "args": "sed -i 's#" + example + "#" + request.data["domain"] + "#g'  " + vhost_dir + request.data["domain"] + "/*"}, \
            "name": "sed_domain" },

            # game.example.com.conf
            {"action": {"module": "file", \
            "args": {"path": www_dir + "web-desktop" + request.data["domain"], "state": "directory"}}, \
            "name": "file_web-desktop" },

            {"action": {"module": "replace", \
            "args": {"path": vhost_dir + request.data["domain"] + "/game." + request.data["domain"] + ".conf", \
            "regexp": old_www_dir + "web-desktophuihuang", \
            "replace": www_dir + "web-desktop" + request.data["domain"]}}, \
            "name": "create_game" },

            {"action": {"module": "replace", \
            "args": {"path": vhost_dir + request.data["domain"] + "/game." + request.data["domain"] + ".conf", \
            "regexp": old_www_dir + "web-mobile-huihuang", \
            "replace": www_dir + "web-mobile-" + request.data["domain"]}}, \
            "name": "create_game_web-desktop-mobile" },

            # g.example.com.conf
            {"action": {"module": "file", \
            "args": {"path": www_dir + "web-mobile-" + request.data["domain"], "state": "directory"}}, \
            "name": "file_g" },

            {"action": {"module": "replace", \
            "args": {"path": vhost_dir + request.data["domain"] + "/g." + request.data["domain"] + ".conf", \
            "regexp": old_www_dir + "web-mobile-huihuang", "replace": www_dir + "web-mobile-" + request.data["domain"]}}, \
            "name": "create_g" },

            #m.example.com.conf
            {"action": {"module": "file", \
            "args": {"path": www_dir + request.data["domain"] + "/h5", "state": "directory"}}, \
            "name": "file_h5" },

            {"action": {"module": "replace", \
            "args": {"path": vhost_dir + request.data["domain"] + "/m." + request.data["domain"] + ".conf", \
            "regexp": old_www_dir + example + "/h5", "replace": www_dir + request.data["domain"] + "/h5"}}, \
            "name": "create_m" },

            #www.example.com.conf
            {"action": {"module": "file", \
            "args": {"path": www_dir + request.data["domain"] + "/pc", "state": "directory"}}, \
            "name": "file_pc" },

            {"action": {"module": "replace", \
            "args": {"path": vhost_dir + request.data["domain"] + "/www." + request.data["domain"] + ".conf", \
            "regexp": old_www_dir + example + "/pc/", "replace": www_dir + request.data["domain"] + "/pc"}}, \
            "name": "create_pc" },
            # 在nginx.conf 主配文件后面加上 include的目录
            {"action": {"module": "replace", \
            "args": {"path": master_nginx_conf, \
            "regexp": "#headinclude", \
            "replace": "#headinclude\r\n  include vhost/" + request.data["domain"] + "/*.conf;"}}, \
            "name": "replace_nginx" },

            # 最后要一个nginx reload 的动作
            ]
        
        ret = runner.run(tasks, "all")
        exechost = ret.results_raw["ok"]["nginx_1"]
        okdomain = {
            request.data["domain"] :
            {
                "stat_lobby":
                {
                    "conf_file": exechost["stat_lobby"]["invocation"]["module_args"]["path"],
                },
                "stat_game":
                {
                    "root_dir": exechost["create_game"]["invocation"]["module_args"]["replace"],
                    "conf_file": exechost["create_game"]["invocation"]["module_args"]["path"],
                },
                "stat_g":
                {
                    "root_dir": exechost["create_g"]["invocation"]["module_args"]["replace"],
                    "conf_file": exechost["create_g"]["invocation"]["module_args"]["path"],
                },
                "stat_m":
                {
                    "root_dir": exechost["create_m"]["invocation"]["module_args"]["replace"],
                    "conf_file": exechost["create_m"]["invocation"]["module_args"]["path"],
                },
                "stat_pc":
                {
                    "root_dir": exechost["create_pc"]["invocation"]["module_args"]["replace"],
                    "conf_file": exechost["create_pc"]["invocation"]["module_args"]["path"],
                },
            },
        }
        return Response(okdomain)

        

class NginxUpdateConfApi(APIView):
    """
    添加conf文件
    """
    def post(self, request):

        return Response(request)

