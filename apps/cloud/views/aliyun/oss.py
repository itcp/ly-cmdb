# ~*~ coding: utf-8 ~*~

from django.shortcuts import render
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_protect
from ops.ansible.runner import AdHocRunner, CommandRunner
from ops.ansible.inventory import BaseInventory
import datetime
import os 
import oss2

package_dir = "/storage/example.com"
bucket_dir = ['regengxin-yfb', 'regengxin-yfb-tmp']
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

auth = oss2.Auth('AccessKeyId', 'AccessKeySecret')

def SyncOssView(request):
    #return HttpResponse("f")
    
    struct_time = datetime.datetime.fromtimestamp(os.path.getmtime(package_dir)) 
    tz_utc_8 = datetime.timezone(datetime.timedelta(hours=8))
    str_time = datetime.datetime.strftime(struct_time.replace(tzinfo=tz_utc_8) ,'%Y-%m-%d %H:%M:%S')
    #str_time = datetime.utcfromtimestamp(struct_time)
    fileIfon = {"file": package_dir, "time": str_time}
    try:
        if request.GET["file"] == "sync":
            for bu in bucket_dir:
                bucket = oss2.Bucket(auth, 'http://oss-cn-hongkong.aliyuncs.com', bu)
                # 同步前先把桶状态设为 private
                rep = bucket.put_bucket_acl('private')
                inventory = BaseInventory(host_data)
                runner = AdHocRunner(inventory)

                tasks = [
                    {"action": {"module": "copy", "args": \
                    {"src": package_dir, "dest": "/root/" + bu + "/"}}, \
                    "name": "copy" }
                ]
                ret = runner.run(tasks, "all")
                # 同步后先把桶状态设为 public
                rep = bucket.put_bucket_acl('public-read')

            
        return HttpResponse(json.dumps({"status": "1"}))
    except:
        return render(request, "aliyun/oss.html", fileIfon)
