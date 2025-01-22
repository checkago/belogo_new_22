# В файле search_indexes.py вашего приложения:

from haystack import indexes
from .models import News, Document


class NewsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)  # Поле для полнотекстового поиска
    name = indexes.CharField(model_attr='name')  # Индекс для поля name
    description = indexes.CharField(model_attr='description')  # Индекс для поля description

    def get_model(self):
        return News

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(published=True)


class DocsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)  # Поле для полнотекстового поиска
    name = indexes.CharField(model_attr='name')  # Индекс для поля name
    description = indexes.CharField(model_attr='description')  # Индекс для поля description

    def get_model(self):
        return Document

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(published=True)