from django.contrib import admin
from django import forms
from mptt.admin import DraggableMPTTAdmin
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from import_export.admin import ImportExportModelAdmin
from web.models import *


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
    prepopulated_fields = {'slug': ('name',)}
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
    list_display = ('name',)


class CinemaAdmin(admin.ModelAdmin):
    list_display = ('name',)


class EventAdmin(admin.ModelAdmin):
    list_display = ('name',)


class BibliotekaAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget(config_name='awesome_ckeditor'))

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
    list_display = ('date', 'fio', 'bilet', 'phone', 'email', 'comment',)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'comment',)


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'comment')


class Service_dop_formAdmin(admin.ModelAdmin):
    list_display = ('fio', 'email', 'comment')


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
    list_display = ('name', 'salary',)


admin.site.register(News, NewsAdmin),
admin.site.register(Document, DocumentAdmin),
admin.site.register(Raiting, RaitingAdmin),
admin.site.register(Shedule, SheduleAdmin),
admin.site.register(Event, EventAdmin),
admin.site.register(Cinema, CinemaAdmin),
admin.site.register(Biblioteka, BibliotekaAdmin),
admin.site.register(Position, PositionAdmin),
admin.site.register(Employers, EmployerAdmin),
admin.site.register(Service_dop, Service_dopAdmin),
admin.site.register(Service, ServiceAdmin),
admin.site.register(Book, BookAdmin),
admin.site.register(Question, QuestionAdmin),
admin.site.register(Feedback, FeedbackAdmin),
admin.site.register(Service_dop_form, Service_dop_formAdmin),
admin.site.register(Partner, PartnerAdmin),
admin.site.register(FreeService, FreeServiceAdmin),
admin.site.register(TermsOfUse, TermsOfUseAdmin),
admin.site.register(Vacancy, VacancyAdmin),
