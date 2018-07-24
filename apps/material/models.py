import hashlib

from django.db import models

from user.models import GuestProfile
from BlogBackendProject.settings import SITE_BASE_URL


class MaterialCategory(models.Model):
    """
    素材类别
    """
    CATEGORY_LEVEL = (
        ("1", "一级类目"),
        ("2", "二级类目"),
        ("3", "三级类目")
    )
    CATEGORY_TYPE = (
        ("articles", "文章总分类"),
        ("articles/category", "文章分类"),
        ("albums", "图集总分类"),
        ("albums/category", "图集分类"),
        ("movies", "电影总分类"),
        ("movies/category", "电影分类"),
        ("readings", "阅读总分类"),
        ("readings/category", "阅读分类"),
        ("books", "书籍总分类"),
        ("books/category", "书籍分类"),
        ("book/notes", "阅读笔记总分类"),
        ("book/notes/category", "阅读笔记分类"),
    )
    name = models.CharField(max_length=30, default="", verbose_name="类别名", help_text="类别名")
    en_name = models.CharField(max_length=30, null=True, blank=True, verbose_name="英文名", help_text="英文名")
    category_type = models.CharField(max_length=30, choices=CATEGORY_TYPE, verbose_name="路由编码", help_text="用于配置路由跳转")
    desc = models.TextField(null=True, blank=True, verbose_name="类别描述", help_text="类别描述")
    en_desc = models.TextField(null=True, blank=True, verbose_name="类别描述", help_text="类别描述")
    image = models.ImageField(upload_to="comment/category/image/%Y/%m", null=True, blank=True, help_text="图片")
    category_level = models.CharField(max_length=20, choices=CATEGORY_LEVEL, verbose_name="类目级别", help_text="类目级别")
    parent_category = models.ForeignKey("self", null=True, blank=True, verbose_name="父类目级别", help_text="父目录",
                                        related_name="sub_category")
    is_active = models.BooleanField(default=True, verbose_name="是否激活", help_text="是否激活")
    is_tab = models.BooleanField(default=True, verbose_name="是否导航", help_text="是否导航")
    index = models.IntegerField(default=0, verbose_name="排序", help_text="排序")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    def save(self, *args, **kwargs):
        # 为英文标题和简介提供默认值
        if not self.en_name:
            self.en_name = self.name
        if not self.en_desc:
            self.en_desc = self.desc
        super(MaterialCategory, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = verbose_name + '列表'

    def __str__(self):
        return '{0} - {1} - {2}'.format(self.name, self.get_category_type_display(), self.get_category_level_display())


class MaterialTag(models.Model):
    """
    素材标签
    """
    name = models.CharField(max_length=30, null=False, blank=False, verbose_name="标签名", help_text="标签名")
    en_name = models.CharField(max_length=30, null=True, blank=True, verbose_name="英文名", help_text="英文名")
    category = models.ForeignKey(MaterialCategory, null=True, blank=True, verbose_name="类别", help_text="类别")
    color = models.CharField(max_length=20, default="blue", verbose_name="颜色", help_text="颜色")
    add_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="添加时间", help_text="添加时间")

    def save(self, *args, **kwargs):
        # 为英文标题和简介提供默认值
        if not self.en_name:
            self.en_name = self.name
        super(MaterialTag, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = verbose_name + '列表'

    def __str__(self):
        return self.name


class MaterialLicense(models.Model):
    """
    素材授权
    """
    COLOR_TYPE = (
        ("#878D99", "灰色"),
        ("#409EFF", "蓝色"),
        ("#67C23A", "绿色"),
        ("#EB9E05", "黄色"),
        ("#FA5555", "红色")
    )
    name = models.CharField(max_length=30, null=False, blank=False, verbose_name="版权名", help_text="版权名")
    en_name = models.CharField(max_length=30, null=True, blank=True, verbose_name="英文名", help_text="英文名")
    desc = models.CharField(max_length=255, null=True, blank=True, verbose_name="简介", help_text="简介")
    en_desc = models.CharField(max_length=255, null=True, blank=True, verbose_name="简介", help_text="简介")
    link = models.URLField(null=True, blank=True, verbose_name="版权参考链接", help_text="版权参考链接")
    color = models.CharField(max_length=20, default="blue", choices=COLOR_TYPE, verbose_name="颜色", help_text="颜色")
    add_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="添加时间", help_text="添加时间")

    def save(self, *args, **kwargs):
        # 为英文标题和简介提供默认值
        if not self.en_name:
            self.en_name = self.name
        if not self.en_desc:
            self.en_desc = self.desc
        super(MaterialLicense, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "授权"
        verbose_name_plural = verbose_name + '列表'

    def __str__(self):
        return self.name


class MaterialCamera(models.Model):
    """
    相机型号
    """
    device = models.CharField(max_length=30, verbose_name="设备", help_text="设备")
    version = models.CharField(max_length=200, verbose_name="版本", help_text="版本")
    environment = models.CharField(max_length=200, verbose_name="环境", help_text="环境")
    add_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="添加时间", help_text="添加时间")

    class Meta:
        verbose_name = "相机型号"
        verbose_name_plural = verbose_name + '列表'

    def __str__(self):
        return self.device


class MaterialPicture(models.Model):
    """
    素材图片
    """
    title = models.CharField(max_length=100, null=False, blank=False, verbose_name="标题", help_text="标题")
    en_title = models.CharField(max_length=100, null=True, blank=True, verbose_name="子标题", help_text="子标题")
    desc = models.CharField(max_length=255, null=True, blank=True, verbose_name="简介", help_text="简介")
    en_desc = models.CharField(max_length=255, null=True, blank=True, verbose_name="摘要", help_text="摘要")
    image = models.ImageField(upload_to="comment/picture/image/%Y/%m", null=True, blank=True, verbose_name="图片",
                              help_text="图片")
    camera = models.ForeignKey(MaterialCamera, null=True, blank=True, verbose_name="拍摄相机", help_text="拍摄相机")
    link = models.URLField(null=True, blank=True, verbose_name="链接", help_text="链接")
    add_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="添加时间", help_text="添加时间")

    def save(self, *args, **kwargs):
        # 为英文标题和简介提供默认值
        if not self.en_title:
            self.en_title = self.title
        if not self.en_desc:
            self.en_desc = self.desc
        super(MaterialPicture, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "图片"
        verbose_name_plural = verbose_name + '列表'

    def __str__(self):
        return self.title


class PostBaseInfo(models.Model):
    """
    Post基本信息
    """
    POST_TYPE = (
        ("article", "文章"),
        ("album", "图集"),
        ("movie", "电影"),
        ("book", "图书"),
        ("book/note", "图书笔记")
    )
    FRONT_IMAGE_TYPE = (
        ("0", "无"),
        ("1", "小图"),
        ("2", "大图")
    )
    title = models.CharField(max_length=100, null=False, blank=False, verbose_name="标题", help_text="标题")
    en_title = models.CharField(max_length=100, null=True, blank=True, verbose_name="英文标题", help_text="英文标题")
    desc = models.CharField(max_length=255, null=True, blank=True, verbose_name="简介", help_text="简介")
    en_desc = models.CharField(max_length=255, null=True, blank=True, verbose_name="英文简介", help_text="英文简介")
    author = models.CharField(max_length=20, null=True, blank=True, verbose_name="作者", help_text="作者")
    category = models.ForeignKey(MaterialCategory, null=False, blank=False, verbose_name="类别", help_text="类别")
    tags = models.ManyToManyField(MaterialTag, through="PostTag", through_fields=('post', 'tag'))
    post_type = models.CharField(max_length=20, choices=POST_TYPE, null=True, blank=True, verbose_name="POST类别",
                                 help_text="POST类别")
    click_num = models.IntegerField(default=0, verbose_name="点击数", help_text="点击数")
    like_num = models.IntegerField(default=0, verbose_name="点赞数", help_text="点赞数")
    comment_num = models.IntegerField(default=0, verbose_name="评论数", help_text="评论数")
    front_image = models.ImageField(upload_to="post/image/%y/%m", null=True, blank=True, verbose_name="封面图",
                                    help_text="大图833*217，小图243*207")
    front_image_type = models.CharField(max_length=20, default="0", choices=FRONT_IMAGE_TYPE, verbose_name="封面图类别",
                                        help_text="封面图类别")
    license = models.ForeignKey(MaterialLicense, null=True, blank=True, verbose_name="版权", help_text="版权")
    is_hot = models.BooleanField(default=False, verbose_name="是否热门", help_text="是否热门")
    is_recommend = models.BooleanField(default=False, verbose_name="是否推荐", help_text="是否推荐")
    is_banner = models.BooleanField(default=False, verbose_name="是否是Banner", help_text="是否是Banner")
    is_active = models.BooleanField(default=True, verbose_name="是否激活", help_text="是否激活")
    is_commentable = models.BooleanField(default=True, verbose_name="是否可评论", help_text="是否可评论")
    browse_password = models.CharField(max_length=20, null=True, blank=True, verbose_name="浏览密码", help_text="浏览密码")
    browse_password_encrypt = models.CharField(max_length=100, null=True, blank=True, verbose_name="浏览密码加密",
                                               help_text="浏览密码加密")
    index = models.IntegerField(default=0, verbose_name="置顶", help_text="置顶")
    add_time = models.DateTimeField(null=True, blank=True, verbose_name="添加时间", help_text="添加时间")

    def save(self, *args, **kwargs):
        # 为英文标题和简介提供默认值
        if not self.en_title:
            self.en_title = self.title
        if not self.en_desc:
            self.en_desc = self.desc
        if self.browse_password and len(self.browse_password) > 0:
            md5 = hashlib.md5()
            md5.update(self.browse_password.encode('utf8'))
            self.browse_password_encrypt = md5.hexdigest()
        else:
            self.browse_password_encrypt = None
        super(PostBaseInfo, self).save(*args, **kwargs)

    # 该方法主要用于RSS中返回文章访问链接
    def get_absolute_url(self):
        return '{0}/{1}/{2}'.format(SITE_BASE_URL, self.post_type, self.id)

    class Meta:
        verbose_name = "所有博文"
        verbose_name_plural = verbose_name + '列表'

    def __str__(self):
        return self.title


class PostTag(models.Model):
    """
    Post标签
    """
    post = models.ForeignKey(PostBaseInfo, null=False, blank=False, verbose_name="文章", help_text="文章")
    tag = models.ForeignKey(MaterialTag, null=False, blank=False, verbose_name="标签", help_text="标签")
    add_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="添加时间", help_text="添加时间")

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = verbose_name + '列表'

    def __str__(self):
        return self.tag.name


class MaterialBanner(models.Model):
    """
    轮播图
    """
    title = models.CharField(max_length=100, verbose_name="标题", help_text="标题")
    en_title = models.CharField(max_length=100, null=True, blank=True, verbose_name="标题", help_text="标题")
    image = models.ImageField(upload_to="comment/banner/image/%y/%m", null=True, blank=True, verbose_name="图片",
                              help_text="图片")
    url = models.URLField(max_length=200, verbose_name="链接", help_text="链接")
    category = models.ForeignKey(MaterialCategory, default='1', null=False, blank=False, verbose_name="类别",
                                 help_text="类别")
    index = models.IntegerField(default=0, verbose_name="顺序", help_text="顺序")
    add_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="添加时间", help_text="添加时间")

    def save(self, *args, **kwargs):
        # 为英文标题和简介提供默认值
        if not self.en_title:
            self.en_title = self.title
        super(MaterialBanner, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name + '列表'

    def __str__(self):
        return self.title


class MaterialSocial(models.Model):
    """
    社交平台
    """
    name = models.CharField(max_length=30, verbose_name="名称", help_text="名称")
    en_name = models.CharField(max_length=30, null=True, blank=True, verbose_name="名称", help_text="名称")
    desc = models.CharField(max_length=100, verbose_name="简介", help_text="简介")
    en_desc = models.CharField(max_length=100, null=True, blank=True, verbose_name="简介", help_text="简介")
    image = models.ImageField(upload_to="comment/social/image/%y/%m", null=True, blank=True, verbose_name="图片",
                              help_text="图片")
    url = models.URLField(max_length=200, verbose_name="链接", help_text="链接")
    add_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="添加时间", help_text="添加时间")

    def save(self, *args, **kwargs):
        # 为英文标题和简介提供默认值
        if not self.en_name:
            self.en_name = self.name
        if not self.en_desc:
            self.en_desc = self.desc
        super(MaterialSocial, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "社交平台"
        verbose_name_plural = verbose_name + '列表'

    def __str__(self):
        return self.name


class MaterialMaster(models.Model):
    """¡
    技能
    """
    name = models.CharField(max_length=30, verbose_name="名称", help_text="名称")
    en_name = models.CharField(max_length=30, null=True, blank=True, verbose_name="名称", help_text="名称")
    desc = models.CharField(max_length=100, null=True, blank=True, verbose_name="简介", help_text="简介")
    en_desc = models.CharField(max_length=100, null=True, blank=True, verbose_name="简介", help_text="简介")
    image = models.ImageField(upload_to="comment/master/image/%y/%m", null=True, blank=True, verbose_name="图片",
                              help_text="图片")
    url = models.URLField(max_length=200, verbose_name="链接", help_text="链接")
    experience = models.FloatField(default=0, verbose_name="熟练度", help_text="熟练度")
    add_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="添加时间", help_text="添加时间")

    def save(self, *args, **kwargs):
        # 为英文标题和简介提供默认值
        if not self.en_name:
            self.en_name = self.name
        if not self.en_desc:
            self.en_desc = self.desc
        super(MaterialMaster, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "技能"
        verbose_name_plural = verbose_name + '列表'

    def __str__(self):
        return self.name
