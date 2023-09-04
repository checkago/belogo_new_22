from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.urls import path
from . import views
from .views import BibliotekiAPIView, NewsAPIView, EventAPIView, ServiceAPIView, \
    WeekView, WeekCDSCHView, WeekBERView, WeekF2View, WeekF3View, WeekF4View, CinemaWeekView, ActiveWeeksAPIView, \
    WeekAPIView, CinemaWeekAPIView, WeekPrint, WeekCDSCHPrint, WeekBERPrint, WeekF2Print, WeekF3Print, WeekF4Print

urlpatterns = [
    path('', views.index, name='index'),
    path('novosti/', views.news, name='news'),
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
    path('brq_form/', views.brq_form, name='brq_form'),
    path('library-category/', views.library_category, name='library_category'),
    path('book-list/1917/', views.library_imperia, name='library_imperia'),
    path('book-list/krai/', views.library_krai, name='library_krai'),
    path('book-list/hud/', views.library_hud, name='library_hud'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book_view'),
    path('events/', views.events, name='events'),
    path('events-archive/', views.events_archive, name='events_archive'),
    path('shedules/', views.shedules, name='shedules'),
    path('mobile-app/', views.mobile, name='mobile-app'),


    # """Schedules"""

    path('schedule_ikc/', WeekView.as_view(), name='schedule_ikc'),
    path('schedule-ikc-print/', WeekPrint.as_view(), name='schedule-ikc-print'),
    path('schedule_cdsch/', WeekCDSCHView.as_view(), name='schedule_cdsch'),
    path('schedule-cdsch-print/', WeekCDSCHPrint.as_view(), name='schedule-cdsch-print'),
    path('schedule_ber/', WeekBERView.as_view(), name='schedule_ber'),
    path('schedule-ber-print/', WeekBERPrint.as_view(), name='schedule-ber-print'),
    path('schedule_f2/', WeekF2View.as_view(), name='schedule_f2'),
    path('schedule-f2-print/', WeekF2Print.as_view(), name='schedule-f2-print'),
    path('schedule_f3/', WeekF3View.as_view(), name='schedule_f3'),
    path('schedule-f3-print/', WeekF3Print.as_view(), name='schedule-f3-print'),
    path('schedule_f4/', WeekF4View.as_view(), name='schedule_f4'),
    path('schedule-f4-print/', WeekF4Print.as_view(), name='schedule-f4-print'),
    path('cinema/', CinemaWeekView.as_view(), name='cinema'),


    # """API List Views"""

    path('api/v1/biblioteka_list/', BibliotekiAPIView.as_view()),
    path('api/v1/news_list/', NewsAPIView.as_view()),
    path('api/v1/event_list/', EventAPIView.as_view()),
    path('api/v1/active-weeks/', ActiveWeeksAPIView.as_view(), name='active-weeks'),
    path('api/v1/week/', WeekAPIView.as_view(), name='week'),
    path('api/v1/cinema-week/', CinemaWeekAPIView.as_view(), name='cinema-week'),
    path('api/v1/services_list/', ServiceAPIView.as_view()),
    path('api/v1/book/create/', views.createBook),
]

if settings.MEDIA_ROOT:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()

handler404 = "web.views.page_not_found_view"
