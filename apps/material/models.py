import hashlib
from django.db import models

from datetime import datetime
import markdown

from user.models import GuestProfile
from utils.RelativeImageExtension import RelativeImageExtension
from BlogBackendProject.settings import MEDIA_URL_PREFIX


class MaterialCategory(models.Model):
    """
    素材类别
    """
    CATEGORY_TYPE = (
        ("1", "一级类目"),
        ("2", "二级类目"),
        ("3", "三级类目")
    )
    name = models.CharField(max_length=30, default="", verbose_name="类别名", help_text="类别名")
    subname = models.CharField(max_length=30, default="", verbose_name="别名", help_text="别名")
    code = models.CharField(max_length=30, default="", verbose_name="code", help_text="code")
    desc = models.TextField(default="", verbose_name="类别描述", help_text="类别描述")
    image = models.ImageField(upload_to="material/category/image/%Y/%m", null=True, blank=True, help_text="图片")
    category_type = models.CharField(max_length=20, choices=CATEGORY_TYPE, verbose_name="类目级别", help_text="类目级别")
    parent_category = models.ForeignKey("self", null=True, blank=True, verbose_name="父类目级别", help_text="父目录",
                                        related_name="sub_category")
    is_tab = models.BooleanField(default=False, verbose_name="是否导航", help_text="是否导航")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = verbose_name + '列表'

    def __str__(self):
        return self.name


class MaterialTag(models.Model):
    """
    素材标签
    """
    COLOR_TYPE = (
        ("blue", "蓝色"),
        ("green", "绿色"),
        ("red", "红色"),
        ("orange", "黄色")
    )
    name = models.CharField(max_length=30, null=False, blank=False, verbose_name="标签名", help_text="标签名")
    subname = models.CharField(max_length=30, null=False, blank=False, verbose_name="标签别名", help_text="标签别名")
    category = models.ForeignKey(MaterialCategory, null=True, blank=True, verbose_name="类别", help_text="类别")
    color = models.CharField(max_length=20, default="blue", choices=COLOR_TYPE, verbose_name="颜色", help_text="颜色")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间", help_text="添加时间")

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
    subname = models.CharField(max_length=30, null=False, blank=False, verbose_name="版权别名", help_text="版权别名")
    desc = models.CharField(max_length=255, null=True, blank=True, verbose_name="简介", help_text="简介")
    link = models.URLField(null=True, blank=True, verbose_name="版权参考链接", help_text="版权参考链接")
    color = models.CharField(max_length=20, default="blue", choices=COLOR_TYPE, verbose_name="颜色", help_text="颜色")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间", help_text="添加时间")

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
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间", help_text="添加时间")

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
    subtitle = models.CharField(max_length=100, null=True, blank=True, verbose_name="子标题", help_text="子标题")
    abstract = models.CharField(max_length=255, null=True, blank=True, verbose_name="摘要", help_text="摘要")
    desc = models.CharField(max_length=255, null=True, blank=True, verbose_name="简介", help_text="简介")
    image = models.ImageField(upload_to="material/picture/image/%Y/%m", null=True, blank=True, verbose_name="图片",
                              help_text="图片")
    camera = models.ForeignKey(MaterialCamera, null=True, blank=True, verbose_name="拍摄相机", help_text="拍摄相机")
    link = models.URLField(null=True, blank=True, verbose_name="链接", help_text="链接")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间", help_text="添加时间")

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
    subtitle = models.CharField(max_length=100, null=True, blank=True, verbose_name="子标题", help_text="子标题")
    abstract = models.CharField(max_length=255, null=True, blank=True, verbose_name="摘要", help_text="摘要")
    desc = models.CharField(max_length=255, null=True, blank=True, verbose_name="简介", help_text="简介")
    author = models.CharField(max_length=20, null=True, blank=True, verbose_name="作者", help_text="作者")
    category = models.ForeignKey(MaterialCategory, null=False, blank=False, verbose_name="类别", help_text="类别")
    tags = models.ManyToManyField(MaterialTag, through="PostTag", through_fields=('post', 'tag'))
    post_type = models.CharField(max_length=20, choices=POST_TYPE, null=True, blank=True, verbose_name="POST类别",
                                 help_text="POST类别")
    click_num = models.IntegerField(default=0, verbose_name="点击数", help_text="点击数")
    like_num = models.IntegerField(default=0, verbose_name="点赞数", help_text="点赞数")
    comment_num = models.IntegerField(default=0, verbose_name="评论数", help_text="评论数")
    front_image = models.ImageField(upload_to="material/post/image/%y/%m", null=True, blank=True, verbose_name="封面图",
                                    help_text="封面图")
    front_image_type = models.CharField(max_length=20, default="0", choices=FRONT_IMAGE_TYPE, verbose_name="封面图类别",
                                        help_text="封面图类别")
    license = models.ForeignKey(MaterialLicense, null=True, blank=True, verbose_name="版权", help_text="版权")
    is_hot = models.BooleanField(default=False, verbose_name="是否热门", help_text="是否热门")
    is_recommend = models.BooleanField(default=False, verbose_name="是否推荐", help_text="是否推荐")
    is_banner = models.BooleanField(default=False, verbose_name="是否是Banner", help_text="是否是Banner")
    is_active = models.BooleanField(default=True, verbose_name="是否激活", help_text="是否激活")
    browse_password = models.CharField(max_length=20, null=True, blank=True, verbose_name="浏览密码", help_text="浏览密码")
    browse_password_encrypt = models.CharField(max_length=100, null=True, blank=True, verbose_name="浏览密码加密",
                                               help_text="浏览密码加密")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间", help_text="添加时间")

    def save(self, *args, **kwargs):
        if self.browse_password:
            md5 = hashlib.md5()
            md5.update(self.browse_password.encode('utf8'))
            self.browse_password_encrypt = md5.hexdigest()
        super(PostBaseInfo, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "所有博文"
        verbose_name_plural = verbose_name + '列表'

    def __str__(self):
        return self.title


class MaterialCommentInfo(models.Model):
    """
    评论基本信息
    """
    post = models.ForeignKey(PostBaseInfo, null=False, blank=False, verbose_name='所属文章')
    author = models.ForeignKey(GuestProfile, null=True, blank=True, related_name="comments", verbose_name='作者')
    reply_to_author = models.ForeignKey(GuestProfile, null=True, blank=True, related_name="be_comments",
                                        verbose_name='被回复人')
    comment_level = models.IntegerField(default=0, verbose_name="评论级别", help_text="评论级别")
    parent_comment = models.ForeignKey("self", null=True, blank=True, related_name="sub_comment", verbose_name="根评论",
                                       help_text="根评论")
    reply_to_comment = models.ForeignKey("self", null=True, blank=True, related_name='reply_comment',
                                         verbose_name='父级评论')
    like_num = models.IntegerField(default=0, verbose_name="点赞数", help_text="点赞数")
    unlike_num = models.IntegerField(default=0, verbose_name="反对数", help_text="反对数")
    comment_num = models.IntegerField(default=0, verbose_name="评论数", help_text="评论数")
    is_hot = models.BooleanField(default=False, verbose_name="是否热门", help_text="是否热门")
    is_recommend = models.BooleanField(default=False, verbose_name="是否推荐", help_text="是否推荐")
    is_active = models.BooleanField(default=True, verbose_name="是否激活", help_text="是否激活")
    # 考虑使用auto_now_add替换生成方式
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间", help_text="添加时间")

    class Meta:
        verbose_name = "评论基本信息"
        verbose_name_plural = verbose_name + '列表'

    def __str__(self):
        return self.detail.formatted_content[:100]


class MaterialCommentDetail(models.Model):
    """
    评论详细信息
    """
    comment_info = models.OneToOneField(MaterialCommentInfo, null=True, blank=True, related_name='detail',
                                        verbose_name="基本信息",
                                        help_text="基本信息")
    origin_content = models.TextField(null=False, blank=False, verbose_name="原始内容", help_text="原始内容")
    formatted_content = models.TextField(null=True, blank=True, verbose_name="处理后内容", help_text="处理后内容")
    update_time = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name="修改时间",
                                       help_text="修改时间")

    def save(self, *args, **kwargs):
        self.formatted_content = markdown.markdown(self.origin_content,
                                                   extensions=[
                                                       'markdown.extensions.extra',
                                                       'markdown.extensions.codehilite',
                                                       'markdown.extensions.toc',
                                                       RelativeImageExtension({
                                                           'base_urls': [
                                                               MEDIA_URL_PREFIX
                                                           ]
                                                       })
                                                   ])
        super(MaterialCommentDetail, self).save(*args, **kwargs)

    def __str__(self):
        return self.comment_info.post.title

    class Meta:
        verbose_name = "评论详细信息"
        verbose_name_plural = verbose_name + '列表'


class PostTag(models.Model):
    """
    Post标签
    """
    post = models.ForeignKey(PostBaseInfo, null=False, blank=False, verbose_name="文章", help_text="文章")
    tag = models.ForeignKey(MaterialTag, null=False, blank=False, verbose_name="标签", help_text="标签")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间", help_text="添加时间")

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
    image = models.ImageField(upload_to="material/banner/image/%y/%m", null=True, blank=True, verbose_name="图片",
                              help_text="图片")
    url = models.URLField(max_length=200, verbose_name="链接", help_text="链接")
    category = models.ForeignKey(MaterialCategory, default='1', null=False, blank=False, verbose_name="类别",
                                 help_text="类别")
    index = models.IntegerField(default=0, verbose_name="顺序", help_text="顺序")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间", help_text="添加时间")

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
    desc = models.CharField(max_length=100, verbose_name="简介", help_text="简介")
    image = models.ImageField(upload_to="material/social/image/%y/%m", null=True, blank=True, verbose_name="图片",
                              help_text="图片")
    url = models.URLField(max_length=200, verbose_name="链接", help_text="链接")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间", help_text="添加时间")

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
    desc = models.CharField(max_length=100, verbose_name="简介", help_text="简介")
    image = models.ImageField(upload_to="material/master/image/%y/%m", null=True, blank=True, verbose_name="图片",
                              help_text="图片")
    url = models.URLField(max_length=200, verbose_name="链接", help_text="链接")
    experience = models.FloatField(default=0, verbose_name="熟练度", help_text="熟练度")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间", help_text="添加时间")

    class Meta:
        verbose_name = "技能"
        verbose_name_plural = verbose_name + '列表'

    def __str__(self):
        return self.name
