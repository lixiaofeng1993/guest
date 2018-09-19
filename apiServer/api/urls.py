# coding=utf-8
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
    # 首页
    url(r'^$', view=views.home, name='home'),

    url(r'^favicon.ico$', RedirectView.as_view(url=r'static/favicon.ico')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
