import hashlib
from django.db import models
from material.models import MaterialSocial, MaterialMaster


class NavigationLink(models.Model):
    """
    自定义导航
    """
    TARGET_TYPE = (
        ("_blank", "blank - 浏览器总在一个新打开、未命名的窗口中载入目标文档。"),
        ("_self",
         "self - 这个目标的值对所有没有指定目标的 <a> 标签是默认目标，它使得目标文档载入并显示在相同的框架或者窗口中作为源文档。这个目标是多余且不必要的，除非和文档标题 <base> 标签中的 target 属性一起使用。"),
        ("_parent", "parent - 这个目标使得文档载入父窗口或者包含来超链接引用的框架的框架集。如果这个引用是在窗口或者在顶级框架中，那么它与目标 _self 等效。"),
        ("_top", "top - 这个目标使得文档载入包含这个超链接的窗口，用 _top 目标将会清除所有被包含的框架并将文档载入整个浏览器窗口。")
    )
    name = models.CharField(max_length=30, verbose_name="名称", help_text="名称")
    en_name = models.CharField(max_length=30, null=True, blank=True, verbose_name="英文名称", help_text="英文名称")
    desc = models.CharField(max_length=100, verbose_name="简介", help_text="简介")
    en_desc = models.CharField(max_length=100, null=True, blank=True, verbose_name="英文简介", help_text="英文简介")
    image = models.ImageField(upload_to="base/friendlink/image/%y/%m", null=True, blank=True, verbose_name="图片",
                              help_text="图片")
    url = models.CharField(max_length=200, verbose_name="链接", help_text="链接")
    target = models.CharField(max_length=10, choices=TARGET_TYPE, null=True, blank=True, verbose_name="Target类别",
                              help_text="对应于a标签中的target属性")
    add_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="添加时间", help_text="添加时间")

    def save(self, *args, **kwargs):
        # 为英文标题和简介提供默认值
        if not self.en_name:
            self.en_name = self.name
        if not self.en_desc:
            self.en_desc = self.desc
        super(NavigationLink, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "自定义导航"
        verbose_name_plural = verbose_name + '列表'

    def __str__(self):
        return self.name


class SiteInfo(models.Model):
    name = models.CharField(default="", max_length=20, verbose_name="名称", help_text="名称")
    en_name = models.CharField(null=True, blank=True, max_length=20, verbose_name="名称英文", help_text="名称英文")
    desc = models.CharField(default="", max_length=150, verbose_name="简介", help_text="简介")
    en_desc = models.CharField(null=True, blank=True, max_length=150, verbose_name="简介", help_text="简介")
    keywords = models.CharField(default="", max_length=300, verbose_name="关键字", help_text="关键字")
    icon = models.ImageField(upload_to="base/site/image/%y/%m", null=True, blank=True, verbose_name="图标",
                             help_text="图标")
    background = models.ImageField(upload_to="base/site/image/%y/%m", null=True, blank=True, verbose_name="背景图",
                                   help_text="背景图")
    api_base_url = models.URLField(max_length=30, null=False, blank=False, verbose_name='API接口BaseURL')
    navigations = models.ManyToManyField(NavigationLink, through="SiteInfoNavigation", through_fields=(
        'site', 'navigation'), verbose_name='自定义导航', help_text='自定义导航')
    copyright = models.CharField(default="", max_length=100, verbose_name="版权", help_text="版权")
    copyright_desc = models.CharField(default="", max_length=300, verbose_name="版权说明中文", help_text="版权说明中文")
    copyright_desc_en = models.CharField(default="", max_length=300, verbose_name="版权说明英文", help_text="版权说明英文")
    icp = models.CharField(default="", max_length=20, verbose_name="ICP", help_text="ICP")
    is_live = models.BooleanField(default=False, verbose_name="是否激活", help_text="是否激活")
    is_force_refresh = models.BooleanField(default=False, verbose_name="是否强制刷新", help_text="用于控制前端页面是否强制刷新本地缓存")
    force_refresh_time = models.DateTimeField(null=True, blank=True, verbose_name="强制刷新时间",
                                              help_text="该时间会返回给前端，前端通过将浏览器本地存储的时间与这个时间进行比对，如果浏览器本地存储的强制刷新时间比这个时间早，就会执行强制刷新浏览器本地缓存")
    access_password = models.CharField(max_length=20, null=True, blank=True, verbose_name="访问密码", help_text="浏览密码")
    access_password_encrypt = models.CharField(max_length=100, null=True, blank=True, verbose_name="浏览密码加密",
                                               help_text="访问密码加密")
    add_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="添加时间", help_text="添加时间")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # 为英文标题和简介提供默认值
        if not self.en_name:
            self.en_name = self.name
        if not self.en_desc:
            self.en_desc = self.desc
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
    en_name = models.CharField(null=True, blank=True, max_length=20, verbose_name="名称英文", help_text="名称英文")
    desc = models.CharField(default="", max_length=300, verbose_name="简介", help_text="简介")
    en_desc = models.CharField(default="", max_length=300, verbose_name="简介", help_text="简介")
    avatar = models.ImageField(upload_to="base/avatar/image/%y/%m", null=True, blank=True, verbose_name="头像",
                               help_text="100*100")
    background = models.ImageField(upload_to="base/background/image/%y/%m", null=True, blank=True, verbose_name="背景图",
                                   help_text="333*125")
    socials = models.ManyToManyField(MaterialSocial, through='BloggerSocial', through_fields=('blogger', 'social'))
    masters = models.ManyToManyField(MaterialMaster, through='BloggerMaster', through_fields=('blogger', 'master'))
    add_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="添加时间", help_text="添加时间")

    def save(self, *args, **kwargs):
        # 为英文标题和简介提供默认值
        if not self.en_name:
            self.en_name = self.name
        if not self.en_desc:
            self.en_desc = self.desc
        super(BloggerInfo, self).save(*args, **kwargs)

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
    image = models.ImageField(upload_to="base/friendlink/image/%y/%m", null=True, blank=True, verbose_name="图片",
                              help_text="图片")
    url = models.URLField(max_length=200, verbose_name="链接", help_text="链接")
    add_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="添加时间", help_text="添加时间")

    class Meta:
        verbose_name = "友情链接"
        verbose_name_plural = verbose_name + '列表'

    def __str__(self):
        return self.name
