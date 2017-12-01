from django.db import models
from datetime import datetime

from django.contrib.auth.models import AbstractUser


# Create your models here.


class UserProfile(AbstractUser):
    """
    用户
    """
    nick_name = models.CharField(max_length=50, default="", verbose_name="昵称", help_text="昵称")
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="姓名", help_text="姓名")
    birthday = models.DateTimeField(null=True, blank=True, verbose_name="生日", help_text="生日")
    gender = models.CharField(max_length=6, choices=(("male", "男"), ("female", "女")), default="female",
                              verbose_name="性别", help_text="性别")
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name="电话", help_text="电话")
    email = models.CharField(max_length=100, null=True, blank=True, verbose_name="邮箱", help_text="邮箱")
    avatar = models.ImageField(upload_to="image/%Y/%m", default="image/default.png", verbose_name="头像", help_text="头像")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间", help_text="添加时间")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def get_unread_nums(self):
        # 在调用时才导入，可以防止循环导入
        # from operation.models import UserMessage
        # return UserMessage.objects.filter(user=self.id, has_read=False).count()
        pass

    def __str__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    """
    邮箱验证码
    """
    CODE_TYPE = (
        ("register", "注册"),
        ("forget", "找回密码"),
        ("update_email", "修改邮箱")
    )

    code = models.CharField(max_length=20, verbose_name="验证码", help_text="验证码")
    email = models.EmailField(max_length=50, verbose_name="邮箱", help_text="邮箱")
    send_type = models.CharField(max_length=15, choices=CODE_TYPE, verbose_name="验证码类型", help_text="验证码类型")
    send_time = models.DateTimeField(default=datetime.now, verbose_name="发送时间", help_text="发送时间")

    class Meta:
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0} [{1}]'.format(self.code, self.email)


class Banner(models.Model):
    """
    轮播图
    """
    title = models.CharField(max_length=100, verbose_name="标题", help_text="标题")
    image = models.ImageField(upload_to="banner/%y/%m", verbose_name="图片", help_text="图片")
    url = models.URLField(max_length=200, verbose_name="链接", help_text="链接")
    index = models.IntegerField(default=100, verbose_name="顺序", help_text="顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间", help_text="添加时间")

    class Meta:
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name
