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
    avatar = models.ImageField(upload_to="user/avatar/image/%Y/%m", null=True, blank=True, verbose_name="头像",
                               help_text="头像")
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


class GuestProfile(models.Model):
    """
    客人
    """
    username = models.CharField(max_length=50, null=True, blank=True, verbose_name="用户名", help_text="用户名")
    nick_name = models.CharField(max_length=50, default="", verbose_name="昵称", help_text="昵称")
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name="电话", help_text="电话")
    email = models.CharField(max_length=100, null=True, blank=True, verbose_name="邮箱", help_text="邮箱")
    avatar = models.ImageField(upload_to="user/avatar/image/%Y/%m", default='user/avatar/image/guest.png', null=True,
                               blank=True, verbose_name="头像", help_text="头像")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间", help_text="添加时间")

    class Meta:
        verbose_name = "客人"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.nick_name


class EmailVerifyRecord(models.Model):
    """
    邮箱验证码
    """
    CODE_TYPE = (
        ("register", "注册"),
        ("forget", "找回密码"),
        ("update_email", "修改邮箱"),
        ("comment", "评论")
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
