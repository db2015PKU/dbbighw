#encoding:utf8
import os,sys;
sys.path.append("./lookmovie");               # 设置项目位置
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")   # 设置环境变量

from django.test.utils import setup_test_environment
from django.test.client import Client
from django.core.urlresolvers import reverse

setup_test_environment()                     # 初始化执行环境
client = Client()                            # 模拟浏览器客户端
response = client.get('/')                   # 发出url"/"的get请求
response.status_code                         # 查看请求状态码  404
response = client.get(reverse('polls:index'))
response.status_code                         # 200
response.content                             # 查看返回的内容
latest_poll_list=response.context['latest_poll_list']; # 查看上下文中的变量内容
latest_poll_list[0];
latest_poll_list[1];
latest_poll_list[1].choice_set;