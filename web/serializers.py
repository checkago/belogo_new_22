from django.utils.html import strip_tags
from rest_framework import serializers
from web.models import Biblioteka, News, Event, Shedule, Service, FreeService, Book


class BibliotekaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Biblioteka
        fields = '__all__'


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'date', 'name', 'description', 'image']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['description'] = strip_tags(instance.description)
        return data


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class SheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shedule
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class FreeServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreeService
        fields = '__all__'


class BookFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'library', 'fio', 'bilet', 'phone', 'email', 'comment']

