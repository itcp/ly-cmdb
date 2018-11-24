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

package_dir = "/storage/dadir"
synclog = "/storage/www/ly-cmdb/sync.log"
exec_sync_bucket = "/storage/www/ly-cmdb/sync_bucket.py"

def readSyncStatus():
    f = open(synclog, 'r')
    result = {}
    for line in f.readlines():
        line = line.strip()
        if not len(line):
            continue
        result[line.split(':')[0]] = line.split(':')[1]
    f.close()
    return result

def SyncOssView(request):
    struct_time = datetime.datetime.fromtimestamp(os.path.getmtime(package_dir)) 
    tz_utc_8 = datetime.timezone(datetime.timedelta(hours=8))
    str_time = datetime.datetime.strftime(struct_time.replace(tzinfo=tz_utc_8) ,'%Y-%m-%d %H:%M:%S')

    fileIfon = {"file": package_dir, "time": str_time, "syncStatus": readSyncStatus()["syncStatus"]}

    try:
        if request.GET["file"] == "sync":
            os.system("python3 " + exec_sync_bucket + " > /dev/null 2>&1 &")

        return HttpResponse(json.dumps({"status": "1"}))
    except:
        return render(request, "aliyun/oss.html", fileIfon)

def getSyncStatus(request):
    syncinfo = readSyncStatus()
    syncStatus = syncinfo["syncStatus"]
    if syncStatus == " sync":
        status = 1
    elif syncStatus == " no":
        status = 0

    return HttpResponse(json.dumps({"status": status, "bucketname": syncinfo["syncingBucket"]}))
