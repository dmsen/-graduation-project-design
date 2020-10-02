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