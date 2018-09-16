"""guest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from sign import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/$', view=views.index, name='index'),  # 登录页面
    url(r'^login_action/$', view=views.login_action, name='login_action'),  # 登录出错跳转
    url(r'^event_manage/$', view=views.event_manage, name='event_manage'),  # 发布会管理
    url(r'^accounts/login/$', view=views.index),  # 验证用户是否登录，未登录跳转到登录页
    url(r'^search_name/$', view=views.search_name, name='search_name'),  # 发布会搜索
    url(r'^guest_manage/$', view=views.guest_manage, name='guest_manage'),  # 嘉宾管理
    url(r'^search_guest/$', view=views.search_guest, name='search_guest'),  # 嘉宾搜索
    url(r'^sign_index/(?P<eid>\d+)/$', view=views.sign_index, name='sign_index'),  # 签到 eid 作为参数传给视图
    url(r'^sign_index_action/(?P<eid>\d+)/$', view=views.sign_index_action, name='sign_index_action'),  # 处理签到操作
    url(r'^logout/$', view=views.logout, name='logout'),  # 退出

    url(r'^api/', include('sign.urls', namespace='sign')),  # api

    url(r'^favicon.ico$', RedirectView.as_view(url=r'static/favicon.ico')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
