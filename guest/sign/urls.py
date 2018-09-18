# coding=utf-8
from django.conf.urls import url
from . import views_api, views_api_sec

urlpatterns = [
    # api
    url(r'^add_event/$', view=views_api.add_event, name='add_event'),  # 添加发布会接口
    url(r'^get_event_list/$', view=views_api.get_event_list, name='get_event_list'),  # 查询发布会接口
    url(r'^add_guest/$', view=views_api.add_guest, name='add_guest'),  # 添加嘉宾接口
    url(r'^get_guest_list/$', view=views_api.get_guest_list, name='get_guest_list'),  # 查询嘉宾接口
    url(r'^user_sign/$', view=views_api.user_sign, name='user_sign'),  # 嘉宾签到接口

    # 加密api
    url(r'^add_event_encode/$', view=views_api_sec.add_event_encode, name='add_event_encode'),  # 添加发布会加密接口
    url(r'^get_event_list_encode/$', view=views_api_sec.get_event_list_encode, name='get_event_list_encode'),  # 查询发布会加密接口
    # url(r'^get_guest_list_encode/$', view=views_api_sec.get_guest_list_encode, name='get_guest_list_encode'),  # 查询嘉宾接口

]
