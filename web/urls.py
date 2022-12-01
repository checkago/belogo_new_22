from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('novosti/<page=1>', views.news, name='news'),
    path('novosti/<int:pk>/', views.news_view, name='news_view'),
    path('biblioteki/', views.biblioteki, name='biblioteki'),
    path('biblioteki/<int:pk>/', views.biblioteka, name='biblioteka'),
    path('documents/', views.documents, name='documents'),
    path('documents/<int:pk>/', views.document, name='document'),
    path('services/', views.services, name='services'),
    path('quality/', views.raitings, name='raitings'),
    path('quality/<int:pk>/', views.raiting, name='raiting'),
    path('vacancy/', views.vacancies, name='vacancies'),
    path('vacancy/<int:pk>/', views.vacancy, name='vacancy'),
    path('fservices/<int:pk>/', views.free_services, name='free_services'),
    path('terms/<int:pk>/', views.termsofuse, name='termsofuse'),
    path('resources/', views.resources, name='resources'),
    path('projects/', views.projects, name='projects'),
    path('contacts/', views.contacts, name='contacts'),
    path('veterany_vov/', views.veterany_vov, name='veterany_vov'),
    path('trujeniki_tyla/', views.veterany_tyla, name='veterany_truda'),
    path('lg_residents_vov/', views.lg_residents, name='lg_residents'),
    path('kniga-pamyati/', views.kniga_pamyati, name='kniga_pamyati'),
    path('book_form/', views.book_form, name='book_form'),
    path('q_form/', views.q_form, name='q_form'),
    path('s_form/', views.s_form, name='s_form'),
    path('library-category/', views.library_category, name='library_category'),
    path('book-list/1917/', views.library_imperia, name='library_imperia'),
    path('book-list/krai/', views.library_krai, name='library_krai'),
    path('book-list/hud/', views.library_hud, name='library_hud'),
    path('library/<int:pk>/', views.book_view, name='book_view'),
    path('events/', views.events, name='events'),
    path('events-archive/', views.events_archive, name='events_archive'),
]


if settings.MEDIA_ROOT:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()

handler404 = "web.views.page_not_found_view"

