# ~*~ coding: utf-8 ~*~

from django.shortcuts import render
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_protect
import os

import unittest
import sys
import re

sys.path.insert(0, "../..")

from ops.ansible.runner import AdHocRunner, CommandRunner
from ops.ansible.inventory import BaseInventory

host_data = [
    {
        "hostname": "keepalived1",
        "ip": "172.20.100.68",
        "port": 22,
        "username": "root",
            "groups": ["keepalived"],
        #"password": "stu@python",
    },
    {
        "hostname": "keepalived2",
        "ip": "172.20.100.71",
        "port": 22,
        "username": "root",
            "groups": ["keepalived"],
        #"password": "stu@python",
    }
]

def keepnet(request):
    return render(request, "architecture/keepnet.html")


class GetKeepIpaddr():
    def setUp(self):
        inventory = BaseInventory(host_data)
        runner = AdHocRunner(inventory)
    
        tasks = [
            {"action": {"module": "shell", "args": "ip addr"}, "name": "ip_addr"},
            {"action": {"module": "shell", "args": "systemctl status keepalived"}, "name": "keepalived_ip" },
        ]
        ret = runner.run(tasks, "all")
        keepIpList = []
        for x,y in ret.results_raw["ok"].items():
            if re.search('Sending gratuitous ARP', y['keepalived_ip']['stdout'].split('\n')[-1]):
                keepIpList.append(
                    [y['keepalived_ip']['stdout'].split('\n')[-1]+ "<br/>++<br/>",
                    y['ip_addr']['stdout'].split('2: eth0')[-1].replace("\n", "<br/>")]
                )
      
        return keepIpList

def get_keep(request):
    if request.is_ajax():
        getIpaddr = GetKeepIpaddr()
        if getIpaddr.setUp() == []:
            receipt = json.dumps({"status": 1, "info": "没有查询到或内部错误！"})
        else:
            receipt = json.dumps({"status": 1, "info": getIpaddr.setUp()})

    return HttpResponse(receipt)
