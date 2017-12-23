from django.db import models

from datetime import datetime

from material.models import MaterialCategory, MaterialTag, PostBaseInfo


# Create your models here.


class ArticleInfo(PostBaseInfo):
    """
    文章基本信息
    """

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = verbose_name + '列表'


class ArticleDetail(models.Model):
    """
    文章基本信息
    """
    article_info = models.OneToOneField(ArticleInfo, null=True, blank=True, related_name='detail', verbose_name="内容", help_text="内容")
    origin_content = models.TextField(null=False, blank=False, verbose_name="原始内容", help_text="原始内容")
    formatted_content = models.TextField(verbose_name="处理后内容", help_text="处理后内容")

    class Meta:
        verbose_name = "文章详情"
        verbose_name_plural = verbose_name + '列表'
