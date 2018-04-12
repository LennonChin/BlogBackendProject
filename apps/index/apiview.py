# _*_ coding: utf-8 _*_
__author__ = 'LennonChin'
__date__ = '2017/12/9 13:31'

from drf_haystack.viewsets import HaystackViewSet

from article.models import ArticleDetail
from material.models import MaterialCommentDetail
from .serializers import SearchSerializer


class SearchViewViewSet(HaystackViewSet):
    """
    搜索ViewSet
    """
    index_models = (ArticleDetail, MaterialCommentDetail)

    serializer_class = SearchSerializer