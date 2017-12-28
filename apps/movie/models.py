import markdown
from django.db import models

from material.models import MaterialCategory, MaterialTag, PostBaseInfo

# Create your models here.


class MovieInfo(PostBaseInfo):
    """
    电影基本信息
    """
    directors = models.CharField(max_length=255, null=True, blank=True, verbose_name="导演", help_text="导演")
    actors = models.CharField(max_length=255, null=True, blank=True, verbose_name="演员", help_text="演员")
    region = models.CharField(max_length=20, null=True, blank=True, verbose_name="地区", help_text="地区")
    language = models.CharField(max_length=20, null=True, blank=True, verbose_name="语言", help_text="语言")
    length = models.IntegerField(default=0, null=True, blank=True, verbose_name="时长", help_text="时长")

    class Meta:
        verbose_name = "电影"
        verbose_name_plural = verbose_name + '列表'

    def __str__(self):
        return self.title


class MovieDetail(models.Model):
    """
    电影详细信息
    """
    movie_info = models.OneToOneField(MovieInfo, null=True, blank=True, related_name='detail', verbose_name="内容", help_text="内容")
    origin_content = models.TextField(null=False, blank=False, verbose_name="原始内容", help_text="原始内容")
    formatted_content = models.TextField(verbose_name="处理后内容", help_text="处理后内容")

    def save(self, *args, **kwargs):
        self.formatted_content = markdown.markdown(self.origin_content,
                                                           extensions=[
                                                               'markdown.extensions.extra',
                                                               'markdown.extensions.codehilite',
                                                               'markdown.extensions.toc'
                                                           ])
        super(MovieDetail, self).save(*args, **kwargs)

    def __str__(self):
        return self.movie_info.title

    class Meta:
        verbose_name = "电影详情"
        verbose_name_plural = verbose_name + '列表'

