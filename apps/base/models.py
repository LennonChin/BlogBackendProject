import hashlib

from django.db import models

from material.models import MaterialSocial, MaterialMaster


class NavigationLink(models.Model):
    """
    自定义导航
    """
    name = models.CharField(max_length=30, verbose_name="名称", help_text="名称")
    desc = models.CharField(max_length=100, verbose_name="简介", help_text="简介")
    image = models.ImageField(upload_to="base/friendlink/image/%y/%m", null=True, blank=True, verbose_name="图片", help_text="图片")
    url = models.URLField(max_length=200, verbose_name="链接", help_text="链接")
    add_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="添加时间", help_text="添加时间")

    class Meta:
        verbose_name = "自定义导航"
        verbose_name_plural = verbose_name + '列表'

    def __str__(self):
        return self.name


class SiteInfo(models.Model):
    name = models.CharField(default="", max_length=20, verbose_name="名称", help_text="名称")
    name_en = models.CharField(default="", max_length=20, verbose_name="名称英文", help_text="名称英文")
    desc = models.CharField(default="", max_length=20, verbose_name="简介", help_text="简介")
    icon = models.ImageField(upload_to="base/site/image/%y/%m", null=True, blank=True, verbose_name="图标", help_text="图标")
    navigations = models.ManyToManyField(NavigationLink, through="SiteInfoNavigation", through_fields=(
        'site', 'navigation'), verbose_name='自定义导航', help_text='自定义导航')
    copyright = models.CharField(default="", max_length=100, verbose_name="版权", help_text="版权")
    icp = models.CharField(default="", max_length=20, verbose_name="ICP", help_text="ICP")
    is_live = models.BooleanField(default=False, verbose_name="是否激活", help_text="是否激活")
    is_force_refresh = models.BooleanField(default=False, verbose_name="是否强制刷新", help_text="是否强制刷新")
    access_password = models.CharField(max_length=20, null=True, blank=True, verbose_name="访问密码", help_text="浏览密码")
    access_password_encrypt = models.CharField(max_length=100, null=True, blank=True, verbose_name="浏览密码加密",
                                               help_text="访问密码加密")
    add_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="添加时间", help_text="添加时间")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.access_password:
            md5 = hashlib.md5()
            md5.update(self.access_password.encode('utf8'))
            self.access_password_encrypt = md5.hexdigest()
        else:
            self.access_password_encrypt = ''
        super(SiteInfo, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "网站信息"
        verbose_name_plural = verbose_name + '列表'


class BloggerInfo(models.Model):
    name = models.CharField(default="", max_length=20, verbose_name="名称", help_text="名称")
    name_en = models.CharField(default="", max_length=20, verbose_name="名称英文", help_text="名称英文")
    desc = models.CharField(default="", max_length=300, verbose_name="简介", help_text="简介")
    avatar = models.ImageField(upload_to="base/avatar/image/%y/%m", null=True, blank=True, verbose_name="头像", help_text="100*100")
    background = models.ImageField(upload_to="base/background/image/%y/%m", null=True, blank=True, verbose_name="背景图", help_text="333*125")
    socials = models.ManyToManyField(MaterialSocial, through='BloggerSocial', through_fields=('blogger', 'social'))
    masters = models.ManyToManyField(MaterialMaster, through='BloggerMaster', through_fields=('blogger', 'master'))
    add_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="添加时间", help_text="添加时间")

    class Meta:
        verbose_name = "个人信息"
        verbose_name_plural = verbose_name + '列表'

    def __str__(self):
        return self.name


class BloggerSocial(models.Model):
    name = models.CharField(default="", max_length=20, verbose_name="名称", help_text="名称")
    blogger = models.ForeignKey(BloggerInfo, verbose_name="个人", help_text="个人")
    social = models.ForeignKey(MaterialSocial, verbose_name="社交平台", help_text="社交平台")
    index = models.IntegerField(default=0, verbose_name="顺序", help_text="顺序")
    add_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="添加时间", help_text="添加时间")

    class Meta:
        verbose_name = "社交信息"
        verbose_name_plural = verbose_name + '列表'

    def __str__(self):
        return self.name


class BloggerMaster(models.Model):
    name = models.CharField(default="", max_length=20, verbose_name="名称", help_text="名称")
    blogger = models.ForeignKey(BloggerInfo, verbose_name="个人", help_text="个人")
    master = models.ForeignKey(MaterialMaster, verbose_name="技能", help_text="技能")
    index = models.IntegerField(default=0, verbose_name="顺序", help_text="顺序")
    add_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="添加时间", help_text="添加时间")

    class Meta:
        verbose_name = "技能信息"
        verbose_name_plural = verbose_name + '列表'

    def __str__(self):
        return self.name


class SiteInfoNavigation(models.Model):
    name = models.CharField(default="", max_length=20, verbose_name="名称", help_text="名称")
    site = models.ForeignKey(SiteInfo, verbose_name="网站", help_text="网站")
    navigation = models.ForeignKey(NavigationLink, verbose_name="导航", help_text="导航")
    index = models.IntegerField(default=0, verbose_name="顺序", help_text="顺序")
    add_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="添加时间", help_text="添加时间")

    class Meta:
        verbose_name = "导航信息"
        verbose_name_plural = verbose_name + '列表'

    def __str__(self):
        return self.name


class FriendLink(models.Model):
    """
    友情链接
    """
    name = models.CharField(max_length=30, verbose_name="名称", help_text="名称")
    desc = models.CharField(max_length=100, verbose_name="简介", help_text="简介")
    image = models.ImageField(upload_to="base/friendlink/image/%y/%m", null=True, blank=True, verbose_name="图片", help_text="图片")
    url = models.URLField(max_length=200, verbose_name="链接", help_text="链接")
    add_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="添加时间", help_text="添加时间")

    class Meta:
        verbose_name = "友情链接"
        verbose_name_plural = verbose_name + '列表'

    def __str__(self):
        return self.name
