from datetime import datetime
from haystack import indexes
from .models import PostBaseInfo


class PostBaseInfoIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    abstract = indexes.CharField(model_attr='abstract')
    desc = indexes.CharField(model_attr='desc')
    add_time = indexes.CharField(model_attr='add_time')

    @staticmethod
    def prepare_autocomplete(obj):
        return " ".join((
            obj.title, obj.abstract, obj.desc
        ))

    def get_model(self):
        return PostBaseInfo

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(add_time__lte=datetime.now())