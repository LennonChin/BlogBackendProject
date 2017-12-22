from django.db import models

from datetime import datetime

from material.models import MaterialCategory, MaterialTag, PostBaseInfo


# Create your models here.


class ArticleInfo(PostBaseInfo):
    """
    文章基本信息
    """
    post_type = models.CharField(max_length=10, default="0", choices=PostBaseInfo.POST_TYPE, verbose_name="POST类别",
                                        help_text="POST类别")
    origin_content = models.TextField(null=False, blank=False, verbose_name="原始内容", help_text="原始内容")
    formatted_content = models.TextField(verbose_name="处理后内容", help_text="处理后内容")

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = verbose_name + '列表'

    def __str__(self):
        return self.title
