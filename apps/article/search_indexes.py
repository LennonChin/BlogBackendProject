from haystack import indexes
from .models import ArticleDetail


class ArticleDetailIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='article_info__title')
    author = indexes.CharField(model_attr='article_info__author')
    add_time = indexes.CharField(model_attr='add_time')
    update_time = indexes.CharField(model_attr='update_time')
    link = indexes.CharField(model_attr='article_info__get_absolute_url')
    type = indexes.CharField(model_attr='article_info__post_type')

    @staticmethod
    def prepare_autocomplete(obj):
        return " "

    def get_model(self):
        return ArticleDetail

    def index_queryset(self, using=None):
        return self.get_model().objects.all()