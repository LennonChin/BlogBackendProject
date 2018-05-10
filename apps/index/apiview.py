# _*_ coding: utf-8 _*_
__author__ = 'LennonChin'
__date__ = '2017/12/9 13:31'

from rest_framework.response import Response
from drf_haystack.viewsets import HaystackViewSet

from article.models import ArticleDetail
from comment.models import CommentDetail
from .serializers import SearchSerializer


class SearchViewViewSet(HaystackViewSet):
    """
    搜索ViewSet
    """
    index_models = (ArticleDetail, CommentDetail)

    serializer_class = SearchSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        raw_datas = serializer.data
        result_data = {}
        for dict in raw_datas:
            type = dict['type']
            if type not in result_data.keys():
                result_data[type] = []
            result_data[type].append(dict)
        return Response(raw_datas)
