from django.contrib import admin
from app01 import models
class linSystemUserAdmin(admin.ModelAdmin):
    # 列表页显示的字段
    list_display = ('userId', 'userName', 'password','jurisdiction','status','remarks' )
    # 可在列表页直接修改（链接和编辑不能同时用）
    list_editable = ('userName', 'password', 'remarks')
    # 可直接点击进入修改页面
    list_display_links = ('userId','jurisdiction','status')
    # 右侧过滤器
    list_filter = ('userId', 'userName', 'password','jurisdiction','status','remarks')
    search_fields = ('userId', 'userName', 'password','jurisdiction','status','remarks')
# Register your models here.

admin.site.register(models.linSystemUser,linSystemUserAdmin)




# 所有网关
class gateways_allAdmin(admin.ModelAdmin):
    # 列表页显示的字段
    list_display = ('gatewayId', 'gatewayName',)
    # 可在列表页直接修改（链接和编辑不能同时用）
    list_editable = ('gatewayName',)
    # 可直接点击进入修改页面
    list_display_links = ('gatewayId',)
    # 右侧过滤器
    list_filter = ('gatewayId', 'gatewayName', )
    search_fields = ('gatewayId', 'gatewayName',  )
# 所有机器监测点
class IOPointsAdmin(admin.ModelAdmin):
    # 列表页显示的字段
    list_display = ('IOPointsId', 'machineName','machineGateway','minRange','maxRange','aline','method','physicalName')
    # 可在列表页直接修改（链接和编辑不能同时用）
    list_editable = ('minRange','maxRange','aline','method','physicalName')
    # 可直接点击进入修改页面
    list_display_links = ('IOPointsId', 'machineName','machineGateway',)
    # 右侧过滤器
    list_filter = ('IOPointsId', 'machineName', 'machineGateway', 'physicalName')
    search_fields = ('IOPointsId', 'machineName', 'machineGateway', 'physicalName')


admin.site.register(models.gateways_all,gateways_allAdmin)
admin.site.register(models.IOPoints,IOPointsAdmin)

# 单个异常记录
class  singleAlarmCodesAdmin(admin.ModelAdmin):
    # 列表页显示的字段
    list_display = ('singleAlarmCodeId', 'startTime','duration','singleAlarmCodeStatus',)
    # 可在列表页直接修改（链接和编辑不能同时用）
    list_editable = ('startTime','duration','singleAlarmCodeStatus')
    # 可直接点击进入修改页面
    list_display_links = ('singleAlarmCodeId',)
    # 右侧过滤器
    list_filter = ('singleAlarmCodeId', 'startTime','duration' )
    search_fields = ('singleAlarmCodeId', 'startTime','duration')
admin.site.register(models.singleAlarmCodes,singleAlarmCodesAdmin)