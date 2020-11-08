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
    url('^linSystem/jsonget$', views.linSystem_jsonGet),
    ##########    实时监测系统     ################
    # 设备类型
    url('^linSystem/machType/get$', views.linSystem_machine_type_get),
    url('^linSystem/machType/add$', views.linSystem_machine_type_add),
    url('^linSystem/machType/mode$', views.linSystem_machine_type_mod),
    url('^linSystem/machType/del$', views.linSystem_machine_type_del),
    # 系统客户
    url('^linSystem/customer/get$', views.linSystem_customer_get),
    url('^linSystem/customer/add$', views.linSystem_customer_add),
    url('^linSystem/customer/mode$', views.linSystem_customer_mod),
    url('^linSystem/customer/del$', views.linSystem_customer_del),
    # 设备
    url('^linSystem/machine/get$', views.linSystem_machine_get),
    url('^linSystem/machine/add$', views.linSystem_machine_add),
    url('^linSystem/machine/mode$', views.linSystem_machine_mod),
    url('^linSystem/machine/del$', views.linSystem_machine_del),
    # 获取所有网关
    url('^linSystem/gwIop/gateways/get', views.linSystem_gateways_get),
    # 所有机器监测点配置查询
    url('^linSystem/gwIopMappingConfig/get$', views.linSystem_machines_IOP_get),
    url('^linSystem/gwIopMappingConfig/add$', views.linSystem_machines_IOP_add),
    url('^linSystem/gwIopMappingConfig/mod$', views.linSystem_machines_IOP_mod),
    url('^linSystem/gwIopMappingConfig/del$', views.linSystem_machines_IOP_del),
    # 根据机器id 查询监测点
    url('^linSystem/machineIdIOP/get$', views.linSystem_gwIopMappingConfig_get),
    # 监测点组配置查询
    url('^linSystem/iopGroup/iopGroups$', views.linSystem_iopgs_get),
    # 异常报警
    # 异常码
    url('^linSystem/alarmCode/get$', views.linSystem_alarmCode_get),
    url('^linSystem/alarmCode/addCodes$', views.linSystem_alarmCodes_add),
    url('^linSystem/alarmCode/modCodes$', views.linSystem_alarmCodes_mod),
    url('^linSystem/alarmCode/delCodes$', views.linSystem_alarmCodes_del),
    # 组合异常码
    url('^linSystem/alarmGroup/get$', views.linSystem_alarmCodesGroup_get),
    # 单个异常记录
    url('^linSystem/singleAlarmCodes/get$', views.linSystem_singleAlarmCodes_get),
    url('^linSystem/singleAlarmCodes/init$', views.linSystem_singleAlarmCodes_init),
    # 所有异常记录
    # url('^linSystem/singleAlarmCodes/getAll$', views.linSystem_singleAlarmCodes_getAll),
    # 解决方案
    url('^linSystem/solution/get$', views.linSystem_solution_get),
    url('^linSystem/solution/add$', views.linSystem_solution_add),
    url('^linSystem/solution/mod$', views.linSystem_solution_mod),
    url('^linSystem/solution/del$', views.linSystem_solution_del),
    #  故障处理接口
    url('^linSystem/alarmProcess$', views.linSystem_alarmProcess),
    url('^linSystem/alarmProcess/history$', views.linSystem_alarmProcess_history),
    # 历史记录highcharts
    url('^linSystem/data/historyDatas$', views.linSystem_historyDatas_get),
    # 历史记录echarts接口1
    url('^linSystem/data/historyDatasLimitCount$', views.linSystem_historyData_echarts_get),
    # 历史记录echarts接口2
    url('^linSystem/data/historyDatasLimitCount2$', views.linSystem_historyData_echarts2_get),
    # 历史记录echarts接口3
    url('^linSystem/data/historyDatasLimitCount3$', views.linSystem_historyData_echarts3_get),
    # 数据对比
    url('^linSystem/data/Contrast$', views.linSystem_contrast_get),
    # 实时传输数据
    url(r'^linSystem/websocket$', views.linSystem_websocket),
    # 标点机构
    # 标点机构
    url('^linSystem/mapPoint/get$', views.linSystem_mapPonit_get),
    url('^linSystem/mapPoint/search$', views.linSystem_mapPonit_search),
    url('^linSystem/mapPointInfo/add$', views.linSystem_mapPonit_add),
    url('^linSystem/mapPoint/add$', views.linSystem_mapPonitImage_add),
    url('^linSystem/mapPoint/imageZan$', views.linSystem_mapPonitImage_zan),
    url('^linSystem/mapPoint/view$', views.linSystem_mapPonit_view),
    url('^linSystem/mapPoint/vedioAdd$', views.linSystem_mapPonitVedio_add),

]
