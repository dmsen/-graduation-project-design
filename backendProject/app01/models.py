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