import markdown
from django.db import models

from material.models import MaterialCategory, MaterialTag, PostBaseInfo
from base.utils import MARKDOWN_EXTENSIONS, MARKDOWN_EXTENSION_CONFIGS


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

    def save(self, *args, **kwargs):
        # 手动设置类型
        self.post_type = 'movie'
        super(MovieInfo, self).save(*args, **kwargs)


class MovieDetail(models.Model):
    """
    电影详细信息
    """
    LANGUAGE = (
        ("CN", "中文"),
        ("EN", "English")
    )
    language = models.CharField(null=True, blank=True, max_length=5, choices=LANGUAGE, verbose_name="文章详情语言类别", help_text="现暂时提供两种语言类别")
    movie_info = models.ForeignKey(MovieInfo, null=True, blank=True, related_name='details', verbose_name="内容",
                                   help_text="内容")
    origin_content = models.TextField(null=False, blank=False, verbose_name="原始内容", help_text="原始内容")
    formatted_content = models.TextField(verbose_name="处理后内容", help_text="处理后内容")
    add_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="添加时间", help_text="添加时间")
    update_time = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name="修改时间",
                                       help_text="修改时间")

    def save(self, *args, **kwargs):
        if not self.language:
            self.language = 'CN'
        self.formatted_content = markdown.markdown(self.origin_content, extensions=MARKDOWN_EXTENSIONS,
                                                   extension_configs=MARKDOWN_EXTENSION_CONFIGS, lazy_ol=False)
        super(MovieDetail, self).save(*args, **kwargs)

    def __str__(self):
        return self.movie_info.title

    class Meta:
        verbose_name = "电影详情"
        verbose_name_plural = verbose_name + '列表'
