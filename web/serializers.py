from rest_framework import serializers
from web.models import Biblioteka, News, Event


class BibliotekaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Biblioteka
        fields = '__all__'


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'date', 'name']


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

