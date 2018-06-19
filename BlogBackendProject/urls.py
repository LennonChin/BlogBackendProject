"""BlogBackendProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import xadmin

from django.conf.urls import url, include
from django.views.static import serve
# from django.contrib import admin

# Django Rest Framework
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

# API路由
from article.apiview import ArticleBaseInfoListViewset, ArticleDetailInfoListViewset
from album.apiview import AlbumBaseInfoListViewset, AlbumDetailInfoListViewset
from movie.apiview import MovieBaseInfoListViewset, MovieDetailInfoListViewset
from book.apiview import BookBaseInfoListViewset, BookDetailInfoListViewset, BookNoteBaseInfoListViewset, BookNoteDetailInfoListViewset
from material.apiview import CategoryListViewset, SingleLevelCategoryListViewset, TagListViewset, \
    MaterialBannerListViewset, PostBaseInfoListViewset, PostLikeViewset, VerifyPostAuthViewset
from comment.apiview import CommentDetailListViewset, CommentLikeViewset
from base.apiview import SiteInfoViewset, BloggerInfoViewset, FriendLinkListViewset
from user.apiview import EmailCodeViewset
from user_operation.apiview import QiniuTokenViewset

from BlogBackendProject.settings import MEDIA_ROOT

from index.views import IndexView
from index.apiview import SearchViewViewSet
from utils.CustomRSS import LatestEntriesFeed
from base.views import SubscribeView, UnSubscribeView

router = DefaultRouter()

# 素材相关
router.register(r'categorys', CategoryListViewset, base_name='categorys')
router.register(r'category', SingleLevelCategoryListViewset, base_name='category')
router.register(r'tags', TagListViewset, base_name='tags')
router.register(r'banners', MaterialBannerListViewset, base_name='banners')

# 文章相关
router.register(r'articleBaseInfos', ArticleBaseInfoListViewset, base_name="articleBaseInfos")
router.register(r'articleDetailInfos', ArticleDetailInfoListViewset, base_name="articleDetailInfos")

# 图集相关
router.register(r'albumBaseInfos', AlbumBaseInfoListViewset, base_name="albumBaseInfos")
router.register(r'albumDetailInfos', AlbumDetailInfoListViewset, base_name="albumDetailInfos")

# 电影
router.register(r'movieBaseInfos', MovieBaseInfoListViewset, base_name="movieBaseInfos")
router.register(r'movieDetailInfos', MovieDetailInfoListViewset, base_name="movieDetailInfos")

# 图书
router.register(r'bookBaseInfos', BookBaseInfoListViewset, base_name='bookBaseInfos')
router.register(r'bookDetailInfos', BookDetailInfoListViewset, base_name='bookDetailInfos')

# 图书笔记
router.register(r'bookNoteBaseInfos', BookNoteBaseInfoListViewset, base_name='bookNoteBaseInfos')
router.register(r'bookNoteDetailInfos', BookNoteDetailInfoListViewset, base_name='bookNoteDetailInfos')

# 时光轴
router.register(r'postBaseInfos', PostBaseInfoListViewset, base_name="postBaseInfos")

# 网站信息
router.register(r'siteInfo', SiteInfoViewset, base_name="siteInfo")
# 博主信息
router.register(r'blogger', BloggerInfoViewset, base_name="blogger")
# 友情链接
router.register(r'friendlinks', FriendLinkListViewset, base_name="friendlinks")
# 评论
router.register(r'comments', CommentDetailListViewset, base_name="comments")
router.register(r'likePost', PostLikeViewset, base_name="likePost")
router.register(r'likeOrUnlikeComment', CommentLikeViewset, base_name="likeOrUnlikeComment")

# 邮箱验证码
router.register(r'emailCode', EmailCodeViewset, base_name="emailCode")
# 验证文章权限
router.register(r'verifyPostAuth', VerifyPostAuthViewset, base_name="verifyPostAuth")
# 七牛云token
router.register(r'qiniuToken', QiniuTokenViewset, base_name='qiniuToken')

# 搜索
router.register("search", SearchViewViewSet, base_name="search")

urlpatterns = [
    # 后台管理
    url(r'^xadmin/', xadmin.site.urls),
    # 媒体文件
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    # RSS订阅
    url(r'^rss/$', LatestEntriesFeed()),
    # 订阅相关
    url(r'^subscribe/$', SubscribeView.as_view(), name='subscribe'),
    url(r'^unsubscribe/$', UnSubscribeView.as_view(), name='unsubscribe'),
    # drf自带认证模式
    url(r'^api-token-auth/', views.obtain_auth_token),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # 文档
    url(r'docs/', include_docs_urls(title="文档", public=False)),
    # 前端页面入口
    url(r'^.*$', IndexView.as_view(), name="index")
]
