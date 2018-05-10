from haystack import indexes
from .models import CommentDetail


class CommentDetailIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='comment_info__post__title')
    author = indexes.CharField(model_attr='comment_info__author__nick_name')
    add_time = indexes.CharField(model_attr='comment_info__add_time')
    type = indexes.CharField(default='comment')
    link = indexes.CharField(model_attr='comment_info__post__get_absolute_url')

    @staticmethod
    def prepare_autocomplete(obj):
        return " "

    def get_model(self):
        return CommentDetail

    def index_queryset(self, using=None):
        return self.get_model().objects.all()