from django.contrib import admin
from django import forms
from mptt.admin import DraggableMPTTAdmin
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
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


class PositionAdmin(admin.ModelAdmin):
    list_display = ('name',)


class EmployerAdmin(admin.ModelAdmin):
    list_display = ('lastname', 'position',)


class EdizmAdmin(admin.ModelAdmin):
    list_display = ('name',)


class Service_dopAdmin(admin.ModelAdmin):
    list_display = ('name', 'price',)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price',)


class BookAdmin(admin.ModelAdmin):
    list_display = ('fio', 'bilet', 'phone', 'email', 'comment',)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'comment',)


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'comment')


class Service_dop_formAdmin(admin.ModelAdmin):
    list_display = ('fio', 'email', 'comment')


class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'link', 'published',)


admin.site.register(News, NewsAdmin),
admin.site.register(Event, EventAdmin),
admin.site.register(Cinema, CinemaAdmin),
admin.site.register(Biblioteka, BibliotekaAdmin),
admin.site.register(Position, PositionAdmin),
admin.site.register(Employers, EmployerAdmin),
admin.site.register(Edizm, EdizmAdmin),
admin.site.register(Service_dop, Service_dopAdmin),
admin.site.register(Service, ServiceAdmin),
admin.site.register(Book, BookAdmin),
admin.site.register(Question, QuestionAdmin),
admin.site.register(Feedback, FeedbackAdmin),
admin.site.register(Service_dop_form, Service_dop_formAdmin),
admin.site.register(Partner, PartnerAdmin),
