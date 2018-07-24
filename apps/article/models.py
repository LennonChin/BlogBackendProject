from django.db import models
import markdown

from material.models import MaterialCategory, MaterialTag, PostBaseInfo
from base.utils import MARKDOWN_EXTENSIONS, MARKDOWN_EXTENSION_CONFIGS


class ArticleInfo(PostBaseInfo):
    """
    文章基本信息
    """

    def save(self, *args, **kwargs):
        self.post_type = 'article'
        super(ArticleInfo, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = verbose_name + '列表'


class ArticleDetail(models.Model):
    """
    文章详细信息
    """
    LANGUAGE = (
        ("CN", "中文"),
        ("EN", "English")
    )
    language = models.CharField(null=True, blank=True, max_length=5, choices=LANGUAGE, verbose_name="文章详情语言类别", help_text="现暂时提供两种语言类别")
    article_info = models.ForeignKey(ArticleInfo, null=True, blank=True, related_name='details', verbose_name="内容", help_text="内容")
    origin_content = models.TextField(null=False, blank=True, verbose_name="原始内容", help_text="原始内容")
    formatted_content = models.TextField(verbose_name="处理后内容", help_text="处理后内容")
    add_time = models.DateTimeField(null=True, blank=True, verbose_name="添加时间", help_text="添加时间")
    update_time = models.DateTimeField(null=True, blank=True, verbose_name="修改时间",
                                       help_text="修改时间")

    def save(self, *args, **kwargs):
        if not self.language:
            self.language = 'CN'
        self.formatted_content = markdown.markdown(self.origin_content, extensions=MARKDOWN_EXTENSIONS,
                                                   extension_configs=MARKDOWN_EXTENSION_CONFIGS, lazy_ol=False)
        super(ArticleDetail, self).save(*args, **kwargs)

    def __str__(self):
        return self.article_info.title

    class Meta:
        verbose_name = "文章详情"
        verbose_name_plural = verbose_name + '列表'
