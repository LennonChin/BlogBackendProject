from django.db import models

from datetime import datetime

from material.models import MaterialCategory, MaterialTag, MaterialPicture, PostBaseInfo


# Create your models here.


class AlbumInfo(PostBaseInfo):
    """
    图集基本信息
    """
    post_type = models.CharField(max_length=10, default="1", choices=PostBaseInfo.POST_TYPE, verbose_name="POST类别",
                                        help_text="POST类别")
    pictures = models.ManyToManyField(MaterialPicture, through="AlbumPhoto", through_fields=('album', 'picture'),
                                      verbose_name="图片", help_text="图片")

    class Meta:
        verbose_name = "图集"
        verbose_name_plural = verbose_name + '列表'

    def __str__(self):
        return self.title


class AlbumPhoto(models.Model):
    """
    图集图片
    """
    album = models.ForeignKey(AlbumInfo, null=False, blank=False, verbose_name="图集", help_text="图集")
    picture = models.ForeignKey(MaterialPicture, null=False, blank=False, verbose_name="图片", help_text="图片")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间", help_text="添加时间")

    class Meta:
        verbose_name = "图集图片"
        verbose_name_plural = verbose_name + '列表'

    def __str__(self):
        return self.album.name
