from django.db import models

from datetime import datetime

from material.models import MaterialCategory, MaterialTag, MaterialPicture


# Create your models here.


class AlbumInfo(models.Model):
    """
    图集基本信息
    """
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
    tags = models.ManyToManyField(MaterialTag, through="AlbumTag", through_fields=('album', 'tag'), verbose_name="标签",
                                  help_text="标签")
    pictures = models.ManyToManyField(MaterialPicture, through="AlbumPhoto", through_fields=('album', 'picture'),
                                      verbose_name="图片", help_text="图片")
    click_num = models.IntegerField(default=0, verbose_name="点击数", help_text="点击数")
    like_num = models.IntegerField(default=0, verbose_name="点赞数", help_text="点击数")
    comment_num = models.IntegerField(default=0, verbose_name="评论数", help_text="评论数")
    front_image = models.ImageField(upload_to="article/images", null=True, blank=True, verbose_name="封面图",
                                    help_text="封面图")
    front_image_type = models.CharField(max_length=20, choices=FRONT_IMAGE_TYPE, verbose_name="封面图类别",
                                        help_text="封面图类别")
    is_hot = models.BooleanField(default=False, verbose_name="是否热门", help_text="是否热门")
    is_recommend = models.BooleanField(default=False, verbose_name="是否推荐", help_text="是否推荐")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间", help_text="添加时间")

    class Meta:
        verbose_name = "图集基本信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class AlbumTag(models.Model):
    """
    图集标签
    """
    album = models.ForeignKey(AlbumInfo, null=False, blank=False, verbose_name="图集", help_text="图集")
    tag = models.ForeignKey(MaterialTag, null=False, blank=False, verbose_name="标签", help_text="标签")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间", help_text="添加时间")

    class Meta:
        verbose_name = "图集标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.album.name


class AlbumPhoto(models.Model):
    """
    图集图片
    """
    album = models.ForeignKey(AlbumInfo, null=False, blank=False, verbose_name="图集", help_text="图集")
    picture = models.ForeignKey(MaterialPicture, null=False, blank=False, verbose_name="图片", help_text="图片")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间", help_text="添加时间")

    class Meta:
        verbose_name = "图集图片"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.album.name
