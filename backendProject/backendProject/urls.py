"""backendProject URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from app01 import views            # 导入app01的视图
from django.views.static import serve
from . import settings
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),
    # 登陆
    url('^linSystem_login$', views.linSystem_login),
    # 系统用户管理
    url('^linSystem/userGet$', views.linSystem_user_get),
    url('^linSystem/userAdd$', views.linSystem_user_add),
    url('^linSystem/userUpdata$', views.linSystem_user_updata),
    url('^linSystem/userDel$', views.linSystem_user_del),
    #     用户通知
    url('^linSystem/notice$', views.linSystem_user_notice),
    # 修改用户头像
    url('^linSystem/modePic$', views.linSystem_userPic_mod),
    # 获取用户未读通知
    url('^linSystem/getNotice$', views.linSystem_user_getNotice),
    # 标记消息已读
    url('^linSystem/readNotice$', views.linSystem_user_readNotice),
    # 获取已读通知
    url('^linSystem/readEdNotice$', views.linSystem_user_readEdNotice),

]
