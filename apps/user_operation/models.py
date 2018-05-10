from django.db import models


class QiniuTokenRecord(models.Model):
    """
    七牛云请求Token
    """
    CODE_TYPE = (
        ("comment", "评论"),
    )

    ip = models.GenericIPAddressField(blank=False, null=False, verbose_name="请求者IP", help_text="请求者IP")
    token = models.CharField(max_length=512, verbose_name="token", help_text="token")
    use_type = models.CharField(max_length=15, choices=CODE_TYPE, verbose_name="使用类型", help_text="使用类型")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="发送时间", help_text="发送时间")

    def __str__(self):
        return '{0} [{1}]'.format(self.ip, self.token)

    class Meta:
        verbose_name = "七牛云请求Token"
        verbose_name_plural = verbose_name
