import os 
import sys
import oss2
import time 

package_dir = sys.argv[0]
bucket_name = sys.argv[1]
synclog = "/storage/cmdb/sync.log"

auth = oss2.Auth('AccessKeyId', 'AccessKeySecret')

starttime = time.strftime("%Y/%m/%d %H-%M-%S", time.localtime())
os.system("sed -i '/start:/c start: " + starttime + "' " + synclog)
os.system("sed -i '/syncStatus:/c syncStatus: sync' " + synclog)

bucket = oss2.Bucket(auth, 'http://oss-cn-hongkong.aliyuncs.com', bucket_name)
# 同步前先把桶状态设为 private
bucket.put_bucket_acl('private')
os.system("sed -i '/bucketStatus:/c bucketStatus: private' " + synclog)
os.system("sed -i '/syncingBucket:/c syncingBucket: " + bucket_name + "' " + synclog)

for parent,dirnames,filenames in os.walk(package_dir):
        for filename in filenames:
                bucket.put_object(parent[1:], b'content of object')
                bucket.put_object(os.path.join(parent,filename)[1:], b'content of object')

    # 同步后先把桶状态设为 public
bucket.put_bucket_acl('public-read')

os.system("sed -i '/syncStatus:/c syncStatus: no' " + synclog)
os.system("sed -i '/bucketStatus:/c bucketStatus: public' " + synclog)
os.system("sed -i '/syncingBucket:/c syncingBucket: no' " + synclog)
endtime = time.strftime("%Y/%m/%d %H-%M-%S", time.localtime())
os.system("sed -i '/end:/c end: " + endtime + "' " + synclog)
