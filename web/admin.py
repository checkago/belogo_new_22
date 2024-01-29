from datetime import timedelta

from django.contrib import admin
from django import forms
from mptt.admin import DraggableMPTTAdmin
from django.contrib.contenttypes.admin import GenericTabularInline
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from import_export.admin import ImportExportModelAdmin
from nested_admin.nested import NestedModelAdmin, NestedTabularInline, NestedInlineModelAdmin

from web.models import ImageGallery, Category, News, Document, Raiting, Biblioteka, FreeService, \
    TermsOfUse, Vacancy, VeteranVOV, VeteranTruda, LeningradResident, HeroMemoryBook, Anons, Shedule, Event, Cinema, \
    Position, Employers, Service_dop, Service, Book, Question, Feedback, Bookrequest, ServiceDop, Partner, Library, \
    Author, LibraryCategory, Week, Eventy, Day, WeekCDSCH, WeekBER, WeekF2, WeekF3, WeekF4, DayCDSCH, \
    EventyCDSCH, EventyBER, DayBER, EventyF2, DayF2, EventyF3, DayF3, EventyF4, DayF4, Movie, CinemaDay, CinemaWeek


class ImageGalleryInline(GenericTabularInline):
    model = ImageGallery
    readonly_fields = ('image_url',)


class CategoryAdmin(DraggableMPTTAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(
    Category,
    CategoryAdmin,
    list_display=(
        'tree_actions',
        'indented_title',
        'get_pages',
    ),
    list_display_links=(
        'indented_title',
    ),
)


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
    prepopulated_fields = {'slug': ('name',)}
    form = DocumentAdminForm
    list_display = ('name', 'published')


class CinemaAdmin(admin.ModelAdmin):
    list_display = ('name',)


class EventAdmin(admin.ModelAdmin):
    list_display = ('name',)


class BibliotekaAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget(config_name='awesome_ckeditor'))

    class Meta:
        verbose_name = 'Текст'
        model = Biblioteka
        fields = '__all__'


class BibliotekaAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    form = BibliotekaAdminForm


class SheduleAdmin(admin.ModelAdmin):
    list_display = ('name',)


class EventAdmin(admin.ModelAdmin):
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
    list_display = ('datetime', 'age', 'school', 'fio', 'bilet', 'phone', 'email', 'comment',)


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
    description = forms.CharField(widget=CKEditorUploadingWidget(config_name='awesome_ckeditor'))

    class Meta:
        verbose_name = 'Описание'
        model = Anons
        fields = '__all__'


class LibraryAdmin(admin.ModelAdmin):
    form = LibraryAdminForm
    list_display = ('title', 'author', 'views')


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


admin.site.register(CinemaWeek, CinemaWeekAdmin)
admin.site.register(Week, WeekAdmin)
admin.site.register(WeekCDSCH, WeekCDSCHAdmin)
admin.site.register(WeekBER, WeekBERAdmin)
admin.site.register(WeekF2, WeekF2Admin)
admin.site.register(WeekF3, WeekF3Admin)
admin.site.register(WeekF4, WeekF4Admin)
admin.site.register(News, NewsAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Raiting, RaitingAdmin)
admin.site.register(Shedule, SheduleAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Cinema, CinemaAdmin)
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
admin.site.register(Anons, AnonsAdmin)
admin.site.register(Library, LibraryAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(LibraryCategory, LibraryCategoryAdmin)


