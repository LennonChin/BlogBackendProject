from datetime import datetime

from django.db import models

from material.models import MaterialCategory, MaterialTag

# Create your models here.


class MovieDetail(models.Model):
    """
    电影详细信息
    """
    origin_content = models.TextField(null=False, blank=False, verbose_name="原始内容", help_text="原始内容")
    formatted_content = models.TextField(null=False, blank=False, verbose_name="处理后内容", help_text="处理后内容")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间", help_text="添加时间")

    class Meta:
        verbose_name = "图片详细信息"
        verbose_name_plural = verbose_name


class MovieInfo(models.Model):
    """
    电影基本信息
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
    directors = models.CharField(max_length=255, null=True, blank=True, verbose_name="导演", help_text="导演")
    actors = models.CharField(max_length=255, null=True, blank=True, verbose_name="演员", help_text="演员")
    category = models.ForeignKey(MaterialCategory, null=False, blank=False, verbose_name="类别", help_text="类别")
    region = models.CharField(max_length=20, null=True, blank=True, verbose_name="地区", help_text="地区")
    language = models.CharField(max_length=20, null=True, blank=True, verbose_name="语言", help_text="语言")
    length = models.IntegerField(default=0, null=True, blank=True, verbose_name="时长", help_text="时长")
    tags = models.ManyToManyField(MaterialTag, through="MovieTag")
    detail = models.ForeignKey(MovieDetail, null=False, blank=False, verbose_name="内容", help_text="内容")
    click_num = models.IntegerField(default=0, verbose_name="点击数", help_text="点击数")
    like_num = models.IntegerField(default=0, verbose_name="点赞数", help_text="点赞数")
    comment_num = models.IntegerField(default=0, verbose_name="评论数", help_text="评论数")
    front_image = models.ImageField(upload_to="article/images", null=True, blank=True, verbose_name="封面图", help_text="封面图")
    front_image_type = models.CharField(max_length=20, choices=FRONT_IMAGE_TYPE, verbose_name="封面图类别",
                                        help_text="封面图类别")
    is_hot = models.BooleanField(default=False, verbose_name="是否热门", help_text="是否热门")
    is_recommend = models.BooleanField(default=False, verbose_name="是否推荐", help_text="是否推荐")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间", help_text="添加时间")

    class Meta:
        verbose_name = "图片基本信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class MovieTag(models.Model):
    """
    电影标签
    """
    movie = models.ForeignKey(MovieInfo, null=False, blank=False, verbose_name="文章")
    tag = models.ForeignKey(MaterialTag, null=False, blank=False, verbose_name="标签")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间", help_text="添加时间")

    class Meta:
        verbose_name = "电影标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.movie.title
