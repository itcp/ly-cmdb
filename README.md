## ly-cmdb

[![Python3](https://img.shields.io/badge/python-3.6-green.svg?style=plastic)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-2.1-brightgreen.svg?style=plastic)](https://www.djangoproject.com/)
[![Ansible](https://img.shields.io/badge/ansible-2.4.2.0-blue.svg?style=plastic)](https://www.ansible.com/)
[![Paramiko](https://img.shields.io/badge/paramiko-2.4.1-green.svg?style=plastic)](http://www.paramiko.org/)


----

基于Jumpserver二次开发的CMDB。线上内部实际运行中。




----

### 功能
在Jumpserver的基础上增加了如下模块

+ onlineconfig	在线配置	
			
			是用来远程自动化配置环境参数的		

+ architecture	架构拓扑
	
			主要是查看业务系统的架构重要参数

+ aliyun	阿里云管理

			用来远程自动化操作阿里云的一些服务


+ nginx conf api	

			运营后台通过 cmdb api 接口生成子站相关配置
