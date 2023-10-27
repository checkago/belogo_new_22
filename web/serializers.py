from django.utils.html import strip_tags
from rest_framework import serializers
from .models import Week, Day, Eventy, WeekCDSCH, DayCDSCH, EventyCDSCH, WeekBER, DayBER, EventyBER, WeekF2, DayF2, \
    EventyF2, WeekF3, DayF3, EventyF3, WeekF4, DayF4, EventyF4, Biblioteka, News, Service, FreeService, Event, Movie, \
    CinemaDay, CinemaWeek


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


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'name', 'library', 'date', 'description', 'image')


class EventySerializer(serializers.ModelSerializer):
    class Meta:
        model = Eventy
        fields = ('id', 'name', 'payment', 'age', 'start_time', 'end_time')


class DaySerializer(serializers.ModelSerializer):
    events = EventySerializer(many=True)

    class Meta:
        model = Day
        fields = ('id', 'name', 'date', 'events')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['events'] = sorted(representation['events'], key=lambda x: x['start_time'])
        return representation


class WeekSerializer(serializers.ModelSerializer):
    days = DaySerializer(many=True)

    class Meta:
        model = Week
        fields = ('id', 'name', 'start_date', 'end_date', 'active', 'days')


class EventyCDSCHSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventyCDSCH
        fields = ('id', 'name', 'payment', 'age', 'start_time', 'end_time')


class DayCDSCHSerializer(serializers.ModelSerializer):
    events = EventyCDSCHSerializer(many=True)

    class Meta:
        model = DayCDSCH
        fields = ('id', 'name', 'date', 'events')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['events'] = sorted(representation['events'], key=lambda x: x['start_time'])
        return representation


class WeekCDSCHSerializer(serializers.ModelSerializer):
    days = DayCDSCHSerializer(many=True)

    class Meta:
        model = WeekCDSCH
        fields = ('id', 'name', 'start_date', 'end_date', 'active', 'days')


class EventyBERSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventyBER
        fields = ('id', 'name', 'payment', 'age', 'start_time', 'end_time')


class DayBERSerializer(serializers.ModelSerializer):
    events = EventyBERSerializer(many=True)

    class Meta:
        model = DayBER
        fields = ('id', 'name', 'date', 'events')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['events'] = sorted(representation['events'], key=lambda x: x['start_time'])
        return representation


class WeekBERSerializer(serializers.ModelSerializer):
    days = DayBERSerializer(many=True)

    class Meta:
        model = WeekBER
        fields = ('id', 'name', 'start_date', 'end_date', 'active', 'days')


class EventyF2Serializer(serializers.ModelSerializer):
    class Meta:
        model = EventyF2
        fields = ('id', 'name', 'payment', 'age', 'start_time', 'end_time')


class DayF2Serializer(serializers.ModelSerializer):
    events = EventyF2Serializer(many=True)

    class Meta:
        model = DayF2
        fields = ('id', 'name', 'date', 'events')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['events'] = sorted(representation['events'], key=lambda x: x['start_time'])
        return representation


class WeekF2Serializer(serializers.ModelSerializer):
    days = DayF2Serializer(many=True)

    class Meta:
        model = WeekF2
        fields = ('id', 'name', 'start_date', 'end_date', 'active', 'days')


class EventyF3Serializer(serializers.ModelSerializer):
    class Meta:
        model = EventyF3
        fields = ('id', 'name', 'payment', 'age', 'start_time', 'end_time')


class DayF3Serializer(serializers.ModelSerializer):
    events = EventyF3Serializer(many=True)

    class Meta:
        model = DayF3
        fields = ('id', 'name', 'date', 'events')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['events'] = sorted(representation['events'], key=lambda x: x['start_time'])
        return representation


class WeekF3Serializer(serializers.ModelSerializer):
    days = DayF3Serializer(many=True)

    class Meta:
        model = WeekF3
        fields = ('id', 'name', 'start_date', 'end_date', 'active', 'days')


class EventyF4Serializer(serializers.ModelSerializer):
    class Meta:
        model = EventyF4
        fields = ('id', 'name', 'payment', 'age', 'start_time', 'end_time')


class DayF4Serializer(serializers.ModelSerializer):
    events = EventyF4Serializer(many=True)

    class Meta:
        model = DayF4
        fields = ('id', 'name', 'date', 'events')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['events'] = sorted(representation['events'], key=lambda x: x['start_time'])
        return representation


class WeekF4Serializer(serializers.ModelSerializer):
    days = DayF4Serializer(many=True)

    class Meta:
        model = WeekF4
        fields = ('id', 'name', 'start_date', 'end_date', 'active', 'days')


class ActiveWeeksSerializer(serializers.Serializer):
    weeks = serializers.SerializerMethodField()

    def get_weeks(self, instance):
        weeks = []

        # Блок 1
        queryset_week = Week.objects.filter(active=True)
        if queryset_week.exists():
            serializer_week = WeekSerializer(queryset_week, many=True)
            weeks.extend(serializer_week.data)

        # Блок 2
        queryset_week_cdsch = WeekCDSCH.objects.filter(active=True)
        if queryset_week_cdsch.exists():
            serializer_week_cdsch = WeekCDSCHSerializer(queryset_week_cdsch, many=True)
            weeks.extend(serializer_week_cdsch.data)

        # Блок 3
        queryset_week_ber = WeekBER.objects.filter(active=True)
        if queryset_week_ber.exists():
            serializer_week_ber = WeekBERSerializer(queryset_week_ber, many=True)
            weeks.extend(serializer_week_ber.data)

        # Блок 4
        queryset_week_f2 = WeekF2.objects.filter(active=True)
        if queryset_week_f2.exists():
            serializer_week_f2 = WeekF2Serializer(queryset_week_f2, many=True)
            weeks.extend(serializer_week_f2.data)

        # Блок 5
        queryset_week_f3 = WeekF3.objects.filter(active=True)
        if queryset_week_f3.exists():
            serializer_week_f3 = WeekF3Serializer(queryset_week_f3, many=True)
            weeks.extend(serializer_week_f3.data)

        # Блок 6
        queryset_week_f4 = WeekF4.objects.filter(active=True)
        if queryset_week_f4.exists():
            serializer_week_f4 = WeekF4Serializer(queryset_week_f4, many=True)
            weeks.extend(serializer_week_f4.data)

        return weeks


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'name', 'start_time')

class CinemaDaySerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True)

    class Meta:
        model = CinemaDay
        fields = ('id', 'name', 'date', 'movies')

class CinemaWeekSerializer(serializers.ModelSerializer):
    cinemadays = CinemaDaySerializer(many=True)

    class Meta:
        model = CinemaWeek
        fields = ('id', 'name', 'start_date', 'end_date', 'active', 'cinemadays')