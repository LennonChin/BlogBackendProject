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
from django.conf.urls import url, include
from django.contrib import admin
import xadmin

# Django Rest Framework
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from article.apiview import ArticleListViewset
from material.apiview import CategoryListViewset

router = DefaultRouter()

# 素材相关
router.register(r'categorys', CategoryListViewset, base_name='categorys')

# 文章相关
router.register(r'articles', ArticleListViewset, base_name="articles")


urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # drf自带认证模式
    url(r'^api-token-auth/', views.obtain_auth_token),
    # 文档
    url(r'docs/', include_docs_urls(title="文档")),
]
