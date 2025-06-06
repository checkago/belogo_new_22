from datetime import timedelta
from datetime import datetime
from django.contrib import admin
from django import forms
from django.db.models.functions import ExtractMonth, ExtractYear
from django.views import View
from mptt.admin import DraggableMPTTAdmin
from django.contrib.contenttypes.admin import GenericTabularInline
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from import_export.admin import ImportExportModelAdmin
from nested_admin.nested import NestedModelAdmin, NestedTabularInline, NestedInlineModelAdmin

from web.models import ImageGallery, Category, News, Document, Raiting, Biblioteka, FreeService, \
    TermsOfUse, Vacancy, VeteranVOV, VeteranTruda, LeningradResident, HeroMemoryBook, Anons, Shedule, Event, Cinema, \
    Position, Employers, Service_dop, Service, Book, Question, Feedback, Bookrequest, ServiceDop, Partner, Library, \
    Author, LibraryCategory, Week, Eventy, Day, WeekCDSCH, WeekBER, WeekF2, WeekF3, WeekF4, DayCDSCH, \
    EventyCDSCH, EventyBER, DayBER, EventyF2, DayF2, EventyF3, DayF3, EventyF4, DayF4, Movie, CinemaDay, CinemaWeek, \
    PolojenieKonkurs, BookView, Project, ProjectTheme, DayB5, WeekB5, EventyCGBT, DayCGBT, EventyBCJ, DayBCJ, \
    EventyBSCD, DayBSCD, EventyYB, DayYB, EventyDB, DayDB, EventyNMB, DayNMB, EventyCSB, DayCSB, EventySSB, DaySSB, \
    EventyFSB, DayFSB, EventyDBT, DayDBT, EventyNAB, DayNAB, EventyPPB, DayPPB, EventyNB, DayNB, WeekCGBT, WeekBCJ, \
    WeekBSCD, WeekYB, WeekDB, WeekNMB, WeekCSB, WeekSSB, WeekFSB, WeekDBT, WeekNAB, WeekPPB, WeekNB, EventyB5, \
    Project_other, Article, AuthorArticle, VideoMemoryBook


class ImageGalleryInline(GenericTabularInline):
    model = ImageGallery
    readonly_fields = ('image_url',)


class CategoryAdmin(DraggableMPTTAdmin):
    list_display = (
        'tree_actions',
        'indented_title',
        'id',
    )
    list_display_links = (
        'indented_title',
    )

admin.site.register(Category, CategoryAdmin)


class NewsAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget(config_name='awesome_ckeditor'))

    class Meta:
        verbose_name = 'Текст'
        model = News
        fields = '__all__'


class NewsAdmin(admin.ModelAdmin):
    inlines = [ImageGalleryInline]
    form = NewsAdminForm
    list_display = ('name', 'category',)


class DocumentAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget(config_name='awesome_ckeditor'))

    class Meta:
        verbose_name = 'Текст'
        model = Document
        fields = '__all__'


class RaitingAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    form = DocumentAdminForm
    list_display = ('name',)


class RaitingAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget(config_name='awesome_ckeditor'))

    class Meta:
        verbose_name = 'Текст'
        model = Raiting
        fields = '__all__'


class DocumentAdmin(admin.ModelAdmin):
    form = DocumentAdminForm
    list_display = ('name', 'category', 'published')
    list_filter = ('category', 'published',)


class PolojenieKonkursAdmin(admin.ModelAdmin):
    form = DocumentAdminForm
    list_display = ('name', 'start_date', 'end_date', 'published', 'category')


class CinemaAdmin(admin.ModelAdmin):
    list_display = ('name',)


class EventAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget(config_name='awesome_ckeditor'), required=False)

    class Meta:
        verbose_name = 'Текст'
        model = Event
        fields = '__all__'


class EventAdmin(admin.ModelAdmin):
    form = EventAdminForm
    list_filter = ('date',)
    list_display = ('name', 'date', 'description', 'id')


class BibliotekaAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget(config_name='awesome_ckeditor'))

    class Meta:
        verbose_name = 'Текст'
        model = Biblioteka
        fields = '__all__'


class BibliotekaAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    form = BibliotekaAdminForm
    list_display = ('name', 'id', 'employer', 'email', 'phone')


class SheduleAdmin(admin.ModelAdmin):
    list_display = ('name',)


class CinemaAdmin(admin.ModelAdmin):
    list_display = ('name',)


class PositionAdmin(admin.ModelAdmin):
    list_display = ('name',)


class EmployerAdmin(admin.ModelAdmin):
    list_display = ('lastname', 'position',)


class Service_dopAdmin(admin.ModelAdmin):
    list_display = ('name', 'price',)


class ServiceAdmin(ImportExportModelAdmin):
    list_display = ('name', 'price',)


class BookAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'fio', 'bilet', 'email', 'comment', 'library')


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'comment',)


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'comment')


class BookrequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'comment')


class ServiceDopAdmin(admin.ModelAdmin):
    list_display = ('fio', 'email', 'date', 'comment', )


class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'link', 'published',)



class FreeServiceAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget(config_name='awesome_ckeditor'))

    class Meta:
        verbose_name = 'Текст'
        model = FreeService
        fields = '__all__'


class FreeServiceAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    form = FreeServiceAdminForm
    list_display = ('id', 'name',)



class TermsOfUseAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget(config_name='awesome_ckeditor'))

    class Meta:
        verbose_name = 'Текст'
        model = TermsOfUse
        fields = '__all__'


class TermsOfUseAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    form = TermsOfUseAdminForm
    list_display = ('id', 'name',)


class VacancyAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget(config_name='awesome_ckeditor'))

    class Meta:
        verbose_name = 'Текст'
        model = Vacancy
        fields = '__all__'


class VacancyAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    form = VacancyAdminForm
    list_display = ('name', 'published', 'salary',)


class VeteranVOVAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget(config_name='awesome_ckeditor'))

    class Meta:
        verbose_name = 'Текст'
        model = VeteranVOV
        fields = '__all__'


class VeteranVOVAdmin(admin.ModelAdmin):
    form = VeteranVOVAdminForm
    list_display = ('last_name', 'first_name', 'middle_name',)


class VeteranTrudaAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget(config_name='awesome_ckeditor'))

    class Meta:
        verbose_name = 'Текст'
        model = VeteranTruda
        fields = '__all__'


class VeteranTrudaAdmin(admin.ModelAdmin):
    form = VeteranTrudaAdminForm
    list_display = ('last_name', 'first_name', 'middle_name',)


class LeningradResidentAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget(config_name='awesome_ckeditor'))

    class Meta:
        verbose_name = 'Текст'
        model = LeningradResident
        fields = '__all__'


class LeningradResidentAdmin(admin.ModelAdmin):
    form = LeningradResidentAdminForm
    list_display = ('last_name', 'first_name', 'middle_name',)


class HeroMemoryBookAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget(config_name='awesome_ckeditor'))

    class Meta:
        verbose_name = 'Текст'
        model = HeroMemoryBook
        fields = '__all__'


class HeroMemoryBookAdmin(admin.ModelAdmin):
    form = HeroMemoryBookAdminForm
    list_display = ('last_name', 'first_name', 'middle_name',)


class VideoMemoryBookAdmin(admin.ModelAdmin):
    list_display = ('title',)


class AnonsAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget(config_name='awesome_ckeditor'))

    class Meta:
        verbose_name = 'Текст'
        model = Anons
        fields = '__all__'


class AnonsAdmin(admin.ModelAdmin):
    form = AnonsAdminForm
    list_display = ('title',)


class LibraryAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget(config_name='awesome_ckeditor'), required=False)

    class Meta:
        verbose_name = 'Описание'
        model = Anons
        fields = '__all__'


@admin.register(BookView)
class BookViewAdmin(admin.ModelAdmin):
    list_display = ('book', 'view_count', 'viewed_at', 'total_views')
    list_filter = ('viewed_at',)
    date_hierarchy = 'viewed_at'
    actions = None  # Отключаем возможность выполнения действий над выбранными объектами

    def total_views(self, obj):
        # Получаем общее количество просмотров для всех книг
        total_views = sum(book.view_count for book in BookView.objects.all())
        return total_views

    total_views.short_description = 'ОБщее колличество просмотров'


class LibraryAdmin(ImportExportModelAdmin):
    form = LibraryAdminForm
    list_display = ('title', 'author', 'views',)



class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)


class LibraryCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class MovieInline(NestedTabularInline):
    model = Movie
    extra = 1


class CinemaDayInline(NestedTabularInline):
    model = CinemaDay
    inlines = [MovieInline]
    extra = 1


class EventyInline(NestedTabularInline):
    model = Eventy
    extra = 1


class DayInline(NestedTabularInline):
    model = Day
    inlines = [EventyInline]
    extra = 1


class EventyCDSCHInline(NestedTabularInline):
    model = EventyCDSCH
    extra = 1


class DayCDSCHInline(NestedTabularInline):
    model = DayCDSCH
    inlines = [EventyCDSCHInline]
    extra = 1


class EventyBERInline(NestedTabularInline):
    model = EventyBER
    extra = 1


class DayBERInline(NestedTabularInline):
    model = DayBER
    inlines = [EventyBERInline]
    extra = 1


class EventyF2Inline(NestedTabularInline):
    model = EventyF2
    extra = 1


class DayF2Inline(NestedTabularInline):
    model = DayF2
    inlines = [EventyF2Inline]
    extra = 1


class EventyF3Inline(NestedTabularInline):
    model = EventyF3
    extra = 1


class DayF3Inline(NestedTabularInline):
    model = DayF3
    inlines = [EventyF3Inline]
    extra = 1


class EventyF4Inline(NestedTabularInline):
    model = EventyF4
    extra = 1


class DayF4Inline(NestedTabularInline):
    model = DayF4
    inlines = [EventyF4Inline]
    extra = 1


class EventyB5Inline(NestedTabularInline):
    model = EventyB5
    extra = 1


class DayB5Inline(NestedTabularInline):
    model = DayB5
    inlines = [EventyB5Inline]
    extra = 1


class EventyCGBTInline(NestedTabularInline):
    model = EventyCGBT
    extra = 1


class DayCGBTInline(NestedTabularInline):
    model = DayCGBT
    inlines = [EventyCGBTInline]
    extra = 1


class EventyBCJInline(NestedTabularInline):
    model = EventyBCJ
    extra = 1


class DayBCJInline(NestedTabularInline):
    model = DayBCJ
    inlines = [EventyBCJInline]
    extra = 1


class EventyBSCDInline(NestedTabularInline):
    model = EventyBSCD
    extra = 1


class DayBSCDInline(NestedTabularInline):
    model = DayBSCD
    inlines = [EventyBSCDInline]
    extra = 1


class EventyYBInline(NestedTabularInline):
    model = EventyYB
    extra = 1


class DayYBInline(NestedTabularInline):
    model = DayYB
    inlines = [EventyYBInline]
    extra = 1


class EventyDBInline(NestedTabularInline):
    model = EventyDB
    extra = 1


class DayDBInline(NestedTabularInline):
    model = DayDB
    inlines = [EventyDBInline]
    extra = 1


class EventyNMBInline(NestedTabularInline):
    model = EventyNMB
    extra = 1


class DayNMBInline(NestedTabularInline):
    model = DayNMB
    inlines = [EventyNMBInline]
    extra = 1


class EventyCSBInline(NestedTabularInline):
    model = EventyCSB
    extra = 1


class DayCSBInline(NestedTabularInline):
    model = DayCSB
    inlines = [EventyCSBInline]
    extra = 1


class EventySSBInline(NestedTabularInline):
    model = EventySSB
    extra = 1


class DaySSBInline(NestedTabularInline):
    model = DaySSB
    inlines = [EventySSBInline]
    extra = 1


class EventyFSBInline(NestedTabularInline):
    model = EventyFSB
    extra = 1


class DayFSBInline(NestedTabularInline):
    model = DayFSB
    inlines = [EventyFSBInline]
    extra = 1


class EventyDBTInline(NestedTabularInline):
    model = EventyDBT
    extra = 1


class DayDBTInline(NestedTabularInline):
    model = DayDBT
    inlines = [EventyDBTInline]
    extra = 1


class EventyNABInline(NestedTabularInline):
    model = EventyNAB
    extra = 1


class DayNABInline(NestedTabularInline):
    model = DayNAB
    inlines = [EventyNABInline]
    extra = 1


class EventyPPBInline(NestedTabularInline):
    model = EventyPPB
    extra = 1


class DayPPBInline(NestedTabularInline):
    model = DayPPB
    inlines = [EventyPPBInline]
    extra = 1


class EventyNBInline(NestedTabularInline):
    model = EventyNB
    extra = 1


class DayNBInline(NestedTabularInline):
    model = DayNB
    inlines = [EventyNBInline]
    extra = 1

def dublicate_week(modeladmin, request, queryset):
    for week in queryset:
        # Получение последнего номера недели
        last_week = week.__class__.objects.order_by('-name').first()
        if last_week:
            last_week_number = int(last_week.name.split()[-1])  # Получить последнее число из названия
            new_week_number = last_week_number + 1
        else:
            new_week_number = 1

        # Вычисление новых дат начала и конца недели
        start_date = week.start_date + timedelta(days=7)
        end_date = week.end_date + timedelta(days=7)

        # Создание копии объекта Week
        new_week = week.__class__.objects.create(
            name=f"Неделя {new_week_number}",
            start_date=start_date,
            end_date=end_date,
            active=False
        )

        # Создание копий связанных объектов Day
        for day in week.days.all():
            new_day = day.__class__.objects.create(
                name=day.name,
                date=day.date + timedelta(days=7),
                week=new_week
            )

            # Создание копий связанных объектов Eventy
            for event in day.events.all():
                event.__class__.objects.create(
                    day=new_day,
                    name=event.name,
                    payment=event.payment,
                    age=event.age,
                    start_time=event.start_time,
                    end_time=event.end_time
                )

dublicate_week.short_description = "Дублировать объект"


def duplicate_cinema_week(modeladmin, request, queryset):
    for cinema_week in queryset:
        # Получение последнего номера недели
        last_cinema_week = cinema_week.__class__.objects.order_by('-name').first()
        if last_cinema_week:
            last_cinema_week_number = int(last_cinema_week.name.split()[-1])  # Получить последнее число из названия
            new_cinema_week_number = last_cinema_week_number + 1
        else:
            new_cinema_week_number = 1

        # Вычисление новых дат начала и конца недели
        start_date = cinema_week.start_date + timedelta(days=7)
        end_date = cinema_week.end_date + timedelta(days=7)

        # Создание копии объекта CinemaWeek
        new_cinema_week = cinema_week.__class__.objects.create(
            name=f"Неделя {new_cinema_week_number}",  # Изменить название нового объекта
            start_date=start_date,
            end_date=end_date,
            active=False
        )

        # Создание копий связанных объектов CinemaDay и Movie
        for cinema_day in cinema_week.cinemadays.all():
            new_cinema_day = cinema_day.__class__.objects.create(
                name=cinema_day.name,
                date=cinema_day.date + timedelta(days=7),
                cinemaweek=new_cinema_week
            )

            for movie in cinema_day.movies.all():
                movie.__class__.objects.create(
                    cinemaday=new_cinema_day,
                    name=movie.name,
                    start_time=movie.start_time
                )

duplicate_cinema_week.short_description = "Дублировать объект"


class CinemaWeekAdmin(NestedModelAdmin):
    actions = [duplicate_cinema_week]
    inlines = [CinemaDayInline]
    exclude = ['active']
    list_display = ('name', 'start_date', 'end_date', 'active')


class WeekAdmin(NestedModelAdmin):
    actions = [dublicate_week]
    inlines = [DayInline]
    exclude = ['active']
    list_display = ('id', 'name', 'start_date', 'end_date', 'active')


class WeekCDSCHAdmin(NestedModelAdmin):
    actions = [dublicate_week]
    inlines = [DayCDSCHInline]
    exclude = ['active']
    list_display = ('name', 'start_date', 'end_date', 'active')


class WeekBERAdmin(NestedModelAdmin):
    actions = [dublicate_week]
    inlines = [DayBERInline]
    exclude = ['active']
    list_display = ('name', 'start_date', 'end_date', 'active')


class WeekF2Admin(NestedModelAdmin):
    actions = [dublicate_week]
    inlines = [DayF2Inline]
    exclude = ['active']
    list_display = ('name', 'start_date', 'end_date', 'active')


class WeekF3Admin(NestedModelAdmin):
    actions = [dublicate_week]
    inlines = [DayF3Inline]
    exclude = ['active']
    list_display = ('name', 'start_date', 'end_date', 'active')


class WeekF4Admin(NestedModelAdmin):
    actions = [dublicate_week]
    inlines = [DayF4Inline]
    exclude = ['active']
    list_display = ('name', 'start_date', 'end_date', 'active')


class WeekB5Admin(NestedModelAdmin):
    actions = [dublicate_week]
    inlines = [DayB5Inline]
    exclude = ['active']
    list_display = ('name', 'start_date', 'end_date', 'active')


class WeekCGBTAdmin(NestedModelAdmin):
    actions = [dublicate_week]
    inlines = [DayCGBTInline]
    exclude = ['active']
    list_display = ('name', 'start_date', 'end_date', 'active')


class WeekBCJAdmin(NestedModelAdmin):
    actions = [dublicate_week]
    inlines = [DayBCJInline]
    exclude = ['active']
    list_display = ('name', 'start_date', 'end_date', 'active')


class WeekBSCDAdmin(NestedModelAdmin):
    actions = [dublicate_week]
    inlines = [DayBSCDInline]
    exclude = ['active']
    list_display = ('name', 'start_date', 'end_date', 'active')


class WeekYBAdmin(NestedModelAdmin):
    actions = [dublicate_week]
    inlines = [DayYBInline]
    exclude = ['active']
    list_display = ('name', 'start_date', 'end_date', 'active')


class WeekDBAdmin(NestedModelAdmin):
    actions = [dublicate_week]
    inlines = [DayDBInline]
    exclude = ['active']
    list_display = ('name', 'start_date', 'end_date', 'active')


class WeekNMBAdmin(NestedModelAdmin):
    actions = [dublicate_week]
    inlines = [DayNMBInline]
    exclude = ['active']
    list_display = ('name', 'start_date', 'end_date', 'active')


class WeekCSBAdmin(NestedModelAdmin):
    actions = [dublicate_week]
    inlines = [DayCSBInline]
    exclude = ['active']
    list_display = ('name', 'start_date', 'end_date', 'active')


class WeekSSBAdmin(NestedModelAdmin):
    actions = [dublicate_week]
    inlines = [DaySSBInline]
    exclude = ['active']
    list_display = ('name', 'start_date', 'end_date', 'active')


class WeekFSBAdmin(NestedModelAdmin):
    actions = [dublicate_week]
    inlines = [DayFSBInline]
    exclude = ['active']
    list_display = ('name', 'start_date', 'end_date', 'active')


class WeekDBTAdmin(NestedModelAdmin):
    actions = [dublicate_week]
    inlines = [DayDBTInline]
    exclude = ['active']
    list_display = ('name', 'start_date', 'end_date', 'active')


class WeekNABAdmin(NestedModelAdmin):
    actions = [dublicate_week]
    inlines = [DayNABInline]
    exclude = ['active']
    list_display = ('name', 'start_date', 'end_date', 'active')


class WeekPPBAdmin(NestedModelAdmin):
    actions = [dublicate_week]
    inlines = [DayPPBInline]
    exclude = ['active']
    list_display = ('name', 'start_date', 'end_date', 'active')


class WeekNBAdmin(NestedModelAdmin):
    actions = [dublicate_week]
    inlines = [DayNBInline]
    exclude = ['active']
    list_display = ('name', 'start_date', 'end_date', 'active')


admin.site.register(CinemaWeek, CinemaWeekAdmin)
admin.site.register(Week, WeekAdmin)
admin.site.register(WeekCDSCH, WeekCDSCHAdmin)
admin.site.register(WeekBER, WeekBERAdmin)
admin.site.register(WeekF2, WeekF2Admin)
admin.site.register(WeekF3, WeekF3Admin)
admin.site.register(WeekF4, WeekF4Admin)
admin.site.register(WeekB5, WeekB5Admin)
admin.site.register(WeekCGBT, WeekCGBTAdmin)
admin.site.register(WeekBCJ, WeekBCJAdmin)
admin.site.register(WeekBSCD, WeekBSCDAdmin)
admin.site.register(WeekYB, WeekYBAdmin)
admin.site.register(WeekDB, WeekDBAdmin)
admin.site.register(WeekNMB, WeekNMBAdmin)
admin.site.register(WeekCSB, WeekCSBAdmin)
admin.site.register(WeekSSB, WeekSSBAdmin)
admin.site.register(WeekFSB, WeekFSBAdmin)
admin.site.register(WeekDBT, WeekDBTAdmin)
admin.site.register(WeekNAB, WeekNABAdmin)
admin.site.register(WeekPPB, WeekPPBAdmin)
admin.site.register(WeekNB, WeekNBAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(PolojenieKonkurs, PolojenieKonkursAdmin)
admin.site.register(Raiting, RaitingAdmin)
admin.site.register(Shedule, SheduleAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Cinema, CinemaAdmin)
admin.site.register(Project)
admin.site.register(ProjectTheme)
admin.site.register(Project_other)
admin.site.register(Article)
admin.site.register(AuthorArticle)
admin.site.register(Biblioteka, BibliotekaAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Employers, EmployerAdmin)
admin.site.register(Service_dop, Service_dopAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(ImageGallery)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Bookrequest, BookrequestAdmin)
admin.site.register(ServiceDop, ServiceDopAdmin)
admin.site.register(Partner, PartnerAdmin)
admin.site.register(FreeService, FreeServiceAdmin)
admin.site.register(TermsOfUse, TermsOfUseAdmin)
admin.site.register(Vacancy, VacancyAdmin)
admin.site.register(VeteranVOV, VeteranVOVAdmin)
admin.site.register(VeteranTruda, VeteranTrudaAdmin)
admin.site.register(LeningradResident, LeningradResidentAdmin)
admin.site.register(HeroMemoryBook, HeroMemoryBookAdmin)
admin.site.register(VideoMemoryBook, VideoMemoryBookAdmin)
admin.site.register(Anons, AnonsAdmin)
admin.site.register(Library, LibraryAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(LibraryCategory, LibraryCategoryAdmin)


