from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from  django.utils.html import format_html

class linSystemUser(models.Model):
    userId = models.AutoField(primary_key=True, verbose_name='用户id')
    userName = models.CharField(max_length=20, verbose_name='用户名',unique=True,null = False,blank = False)
    password = models.CharField(max_length=20, verbose_name='密码')
    userPic = models.ImageField(upload_to='./linSystem/%Y/%m%d/', verbose_name='linSystemUser头像',default='/linSystem/defaultTou.png')
    USER_CHOICE = (
        (0, 0),
        (1, 1),
        (2,2),
        (3, 3),
    )
    USER_STATUS = (
        (0, 0),
        (1, 1),
    )
    jurisdiction = models.IntegerField(choices=USER_CHOICE, verbose_name='权限等级',default=1)
    status = models.IntegerField(choices=USER_STATUS, verbose_name='用户状态',default=1)
    remarks = models.CharField(max_length=10, verbose_name='备注',null = True,blank = False)
    # 可以在django后台显示
    # def __str__(self):
    #     return self.userName
    # def image_data(self):
    #     return format_html(
    #         self.userPic.url
    #     )
    def toDict(self):
        return dict([(attr, getattr(self, attr)) for attr in
                     [f.name for f in self._meta.fields]])  # type(self._meta.fields).__name__
    class Meta:
        verbose_name = "linSystem用户"
        verbose_name_plural = verbose_name
        db_table = ''
        ordering = ['-userId']
# 删除之前的图片，避免 图片冗杂
@receiver(pre_delete, sender=linSystemUser)
# sender = 你要修改图片字段所在的类
def file_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    # print('进入文件删除方法，删的是',instance.alter_file)
    instance.userPic.delete(False)


# 用户通知
class linSystemNotice(models.Model):
    """通知"""
    import django.utils.timezone as timezone
    linSystemNoticeId = models.AutoField(primary_key=True, verbose_name='通知id')
    msg  = models.TextField(max_length=200,verbose_name='通知内容')
    CHOICE = (
        (0, 0),
        (1, 1),
    )
    status =  models.IntegerField(choices=CHOICE,verbose_name = '通知状态',default=0)
    courseEvaluateDate = models.DateTimeField(default=timezone.now, verbose_name='通知时间')
    byPerson = models.CharField(verbose_name='发布通知者',default="lin",max_length=10)
    # 默认级联删除
    linSystemNoticeUser = models.ForeignKey(linSystemUser, verbose_name='通知人',on_delete=models.CASCADE)
    class Meta:
        verbose_name = "linSystem通知"
        verbose_name_plural = verbose_name
        db_table = 'linSystem通知'
    def toDict(self):
        return dict([(attr, getattr(self, attr)) for attr in
                     [f.name for f in self._meta.fields]])


##########################    实时监测系统   ##################################
# 设备类型
class machTypes(models.Model):
    machTypeId = models.AutoField(primary_key=True, verbose_name='机器类型id')
    machTypeCode = models.CharField(max_length=10, verbose_name='机器类型编号', default="defaultTypeCode")
    machTypeName = models.CharField(max_length=10, verbose_name='机器类型名称',unique=True)
    machTypeDesc = models.CharField(max_length=30, verbose_name='机器类型描述')

    # def __str__(self):
    #     return self.machTypeCode

    def toDict(self):
        return dict([(attr, getattr(self, attr)) for attr in
                     [f.name for f in self._meta.fields]])  # type(self._meta.fields).__name__

    class Meta:
        verbose_name = "机器类型"
        verbose_name_plural = verbose_name
        db_table = '机器类型'
        ordering = ['machTypeId']
# 客户
class customers(models.Model):
    customerId= models.AutoField(primary_key=True,verbose_name = '顾客id')
    customerName= models.CharField(max_length=10,verbose_name = '顾客名',unique=True)
    customerType= models.CharField(max_length = 30,verbose_name = '顾客类型')
    CHOICE = (
        (1, 1),
        (1, 0),
    )
    customerLevel= models.IntegerField(choices=CHOICE,verbose_name = '顾客等级')
    sponsor= models.CharField(max_length = 6,verbose_name = '赞助商')
    phone= models.CharField(max_length=11,verbose_name = '联系电话')
    address= models.CharField(max_length = 10,verbose_name = '地址')
    machCount= models.IntegerField(verbose_name = '机器数目')
    remark= models.CharField(max_length=10,verbose_name = 'remark')
    def __str__(self):
        return self.customerName
    def toDict(self):
        return dict([(attr, getattr(self, attr)) for attr in
                     [f.name for f in self._meta.fields]])  # type(self._meta.fields).__name__
    class Meta:
        verbose_name = "客户"
        verbose_name_plural = verbose_name
        db_table = '客户'
        ordering = ['customerId']
# 设备
class machines(models.Model):
    import django.utils.timezone as timezone
    # AutoField :自增型字段（值自增）----int
    machineId= models.AutoField(primary_key=True,verbose_name = '机器id') #合法
    # CharField 文本型字段---》varchar
    # 必填项：max_length:最大字符长度（max_length将在数据库层和Django表单验证中起作用）
    machineName= models.CharField(max_length=10,verbose_name = '机器名称',unique=True)
    # IntegerField()：整型字段
    # machTypeId= models.IntegerField(max_length=10,verbose_name = '机器类型id')
    machTypeId = models.ForeignKey(machTypes, verbose_name='机器类型id',related_name='machine_machTypeId',on_delete=models.CASCADE)
    # machTypeId = models.OneToOneField(machTypes, verbose_name='机器类型id')
    machineDesc = models.TextField(max_length = 30,verbose_name = '机器描述')
    # DateField :日期型字段
    # DateTimeField： 日期时间型字段
    #二个属性
    #auto_now_add: insert 的时候会更新这个字段
    # auto_now:insert/update 的时候会更新这个值
    dataOfProdect= models.DateTimeField(default = timezone.now,verbose_name = '生产日期')
    office = models.CharField(max_length = 10,verbose_name = '办事处')
    mwordId = models.IntegerField(verbose_name = 'mworkid',default=1)
    customerName = models.ForeignKey(customers, verbose_name='客户',related_name='customers_customerName',on_delete=models.CASCADE)
    # def __str__(self):
    #     return self.machineName

    def toDict(self):
        return dict([(attr, getattr(self, attr)) for attr in
                     [f.name for f in self._meta.fields]])  # type(self._meta.fields).__name__
    class Meta:
        verbose_name = "机器/设备"
        verbose_name_plural = verbose_name
        db_table = '设备'
        ordering = ['machineId']


# # 所有监测点
# class IOPoints_all(models.Model):
#     IOPId = models.AutoField(primary_key=True, verbose_name='监测点')
#     IOPName= models.CharField(max_length = 30,verbose_name = '监测点名',unique = True)
#
#     def __str__(self):
#         return self.IOPName
#     class Meta:
#         verbose_name = "所有监测点"
#         verbose_name_plural = verbose_name
#         db_table = '所有监测点'
#         ordering = ['IOPId']
# 所有网关
class  gateways_all(models.Model):
    gatewayId = models.AutoField(primary_key=True, verbose_name='网关Id')
    gatewayName= models.CharField(max_length = 30,verbose_name = '网关名',unique = True)
    # IOPNames = models.ManyToManyField(IOPoints_all,verbose_name = '监测点名',related_name='iopname')
    def __str__(self):
        return self.gatewayName

    def toDict(self):
        return dict([(attr, getattr(self, attr)) for attr in
                     [f.name for f in self._meta.fields]])  # type(self._meta.fields).__name__
    class Meta:
        verbose_name = "所有网关"
        verbose_name_plural = verbose_name
        db_table = '所有网关'
        ordering = ['gatewayId']
# 机器监测点
class IOPoints(models.Model):
    IOPointsId= models.AutoField(primary_key=True,verbose_name = '机器监测点id')
    physicalName = models.CharField(max_length = 16,verbose_name = '机器监测点物理名称',unique = True)
    machineName = models.ForeignKey(machines,verbose_name = '机器名',on_delete=models.CASCADE)
    machineGateway = models.ForeignKey(gateways_all,verbose_name = '网关',on_delete=models.CASCADE)
    minRange = models.IntegerField(verbose_name = '最小量程',null = True,blank = True,default = 0)
    maxRange = models.IntegerField(verbose_name='最大量程', null=False, blank=False)
    aline = models.IntegerField(verbose_name='校准值', null=True,blank = True)
    method = models.IntegerField(verbose_name='计算方式', null=True,blank = True,default = 1)
    def toDict(self):
        return dict([(attr, getattr(self, attr)) for attr in
                     [f.name for f in self._meta.fields]])  # type(self._meta.fields).__name__
    def __str__(self):
        return self.physicalName
    class Meta:
        verbose_name = "所有机器监测点"
        verbose_name_plural = verbose_name
        db_table = '所有机器监测点'
        ordering = ['IOPointsId']


# 异常码
class alarmCodes(models.Model):
    alarmCodeId= models.CharField(max_length = 16,primary_key=True,verbose_name = '异常码id',unique = True)
    alarmCodeName = models.CharField(max_length = 16,verbose_name = '异常码名字')
    machineName = models.ForeignKey(machines,verbose_name = '机器名',on_delete=models.CASCADE)
    physicalName = models.ForeignKey(IOPoints, verbose_name='监控点物理量',on_delete=models.CASCADE)
    minValue = models.IntegerField(verbose_name = '最小值',null = False,blank = False,default = 0)
    maxValue = models.IntegerField(verbose_name='最大值', null=False, blank=False)
    alarmMsg = models.CharField(max_length = 36,verbose_name='异常信息', null=True,blank = True)
    level = models.IntegerField(verbose_name='异常级别', null=True,blank = True,default = 1)
    timeLimit = models.IntegerField(verbose_name='异常时延', null=True, blank=True, default=10)
    # def __str__(self):
    #     return self.alarmCodeName
    def toDict(self):
        return dict([(attr, getattr(self, attr)) for attr in
                     [f.name for f in self._meta.fields]])  # type(self._meta.fields).__name__
    class Meta:
        verbose_name = "异常码"
        verbose_name_plural = verbose_name
        db_table = '异常码'
        ordering = ['alarmCodeId']

#  单个异常记录
class singleAlarmCodes(models.Model):
    import django.utils.timezone as timezone
    singleAlarmCodeId= models.AutoField(primary_key=True,verbose_name = '单个异常记录id')
    machineName = models.ForeignKey(machines,verbose_name = '机器名',on_delete=models.CASCADE)
    alarmCodeName = models.ForeignKey(alarmCodes, verbose_name='异常码名字',on_delete=models.CASCADE)
    startTime= models.DateTimeField(default = timezone.now,verbose_name = '开始时间')
    duration = models.IntegerField(verbose_name='持续时间', null=True, blank=True, default=10)
    singleAlarmCodeStatus = models.IntegerField(verbose_name='异常记录状态', default=0)
    def toDict(self):
        return dict([(attr, getattr(self, attr)) for attr in
                     [f.name for f in self._meta.fields]])  # type(self._meta.fields).__name__
    class Meta:
        verbose_name = "单个异常记录"
        verbose_name_plural = verbose_name
        db_table = '单个异常记录'
        ordering = ['singleAlarmCodeId']

#  异常处理历史
class alarmProcessHistory(models.Model):
    alarmProcessHistoryId= models.AutoField(primary_key=True,verbose_name = '异常处理历史id')
    alarmCode = models.CharField(max_length=16, verbose_name='异常码编号', null=True, blank=True)
    alarmCodeName = models.CharField(max_length = 16,verbose_name = '异常码名称',null=True,blank=True)
    alarmSolutonId = models.CharField(max_length=32, verbose_name='解决方案编号', null=True, blank=True)
    # alarmSolutonName = models.CharField(max_length = 32, verbose_name='解决方案名称',null=True,blank=True)
    callbackMsg= models.TextField(verbose_name = '反馈信息',null=True,blank=True)
    processTime = models.DateTimeField(auto_now_add = True, verbose_name='处理时间')
    machineName = models.CharField(max_length = 16, verbose_name='机器名称',null=True,blank=True)
    def toDict(self):
        return dict([(attr, getattr(self, attr)) for attr in
                     [f.name for f in self._meta.fields]])  # type(self._meta.fields).__name__
    class Meta:
        verbose_name = "异常处理历史"
        verbose_name_plural = verbose_name
        db_table = '异常处理历史'
        ordering = ['alarmProcessHistoryId']

#  解决方案
class alarmSolutons(models.Model):
    alarmSolutonId= models.AutoField(primary_key=True,verbose_name = '解决方案id')
    alarmSolutonName = models.CharField(max_length = 32,verbose_name = '解决方案名称',unique=True)
    alarmSolutonDetail = models.CharField(max_length = 32, verbose_name='解决方案描述')
    alarmCodeList= models.TextField(verbose_name = '适用与异常码/组合码')
    def toDict(self):
        return dict([(attr, getattr(self, attr)) for attr in
                     [f.name for f in self._meta.fields]])  # type(self._meta.fields).__name__
    class Meta:
        verbose_name = "解决方案"
        verbose_name_plural = verbose_name
        db_table = '解决方案'
        ordering = ['alarmSolutonId']
