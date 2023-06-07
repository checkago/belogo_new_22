from django.utils.html import strip_tags
from rest_framework import serializers
from web.models import Biblioteka, DayEvent, News, Event, Shedule, Service, FreeService, Book, Category, SheduleDay


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


class BookFormSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    library = serializers.CharField()
    fio = serializers.CharField()
    bilet = serializers.CharField()
    phone = serializers.CharField()
    email = serializers.EmailField()
    comment = serializers.CharField()


class DayEventSerializer(serializers.ModelSerializer):
    start_time = serializers.TimeField(format='%H:%M')
    end_time = serializers.TimeField(format='%H:%M')

    class Meta:
        model = DayEvent
        fields = ('id', 'name', 'start_time', 'end_time')


class SheduleDaySerializer(serializers.ModelSerializer): 
    events_list = DayEventSerializer(many=True)
    date = serializers.DateField(format='%J %F')

    class Meta: 
        model = SheduleDay 
        fields = ('id', 'name', 'date', 'events_list')


class SheduleDayBERSerializer(serializers.ModelSerializer): 
    events_list = DayEventSerializer(many=True) 
 
    class Meta: 
        model = SheduleDay 
        fields = ('id', 'name', 'date', 'events_list')


class SheduleDayCDSCHSerializer(serializers.ModelSerializer): 
    events_list = DayEventSerializer(many=True) 
 
    class Meta: 
        model = SheduleDay 
        fields = ('id', 'name', 'date', 'events_list')


class SheduleDayF2Serializer(serializers.ModelSerializer): 
    events_list = DayEventSerializer(many=True) 
 
    class Meta: 
        model = SheduleDay 
        fields = ('id', 'name', 'date', 'events_list')


class SheduleDayF3Serializer(serializers.ModelSerializer): 
    events_list = DayEventSerializer(many=True) 
 
    class Meta: 
        model = SheduleDay 
        fields = ('id', 'name', 'date', 'events_list')


class SheduleDayF4Serializer(serializers.ModelSerializer): 
    events_list = DayEventSerializer(many=True) 
 
    class Meta: 
        model = SheduleDay 
        fields = ('id', 'name', 'date', 'events_list')