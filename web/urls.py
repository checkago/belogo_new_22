from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.urls import path
from django.views.generic import RedirectView

from . import views
from .views import BibliotekiAPIView, NewsAPIView, EventAPIView, ServiceAPIView, \
    WeekView, WeekCDSCHView, WeekBERView, WeekF2View, WeekF3View, WeekF4View, CinemaWeekView, ActiveWeeksAPIView, \
    WeekAPIView, CinemaWeekAPIView, WeekPrint, WeekCDSCHPrint, WeekBERPrint, WeekF2Print, WeekF3Print, WeekF4Print, \
    CinemaWeekPrint, WeekVertical, WeekCDSCHVertical, WeekBERVertical, WeekF2Vertical, WeekF3Vertical, WeekF4Vertical, \
    WeekB5View, WeekB5Print, WeekB5Vertical, WeekCGBTView, WeekCGBTPrint, WeekCGBTVertical, WeekBCJView, WeekBCJPrint, \
    WeekBCJVertical, WeekBSCDView, WeekBSCDPrint, WeekBSCDVertical, WeekYBView, WeekYBPrint, WeekYBVertical, WeekDBView, \
    WeekDBPrint, WeekDBVertical, WeekNMBView, WeekNMBPrint, WeekNMBVertical, WeekCSBView, WeekCSBPrint, WeekCSBVertical, \
    WeekSSBView, WeekSSBPrint, WeekSSBVertical, WeekFSBView, WeekFSBPrint, WeekDBTView, WeekFSBVertical, WeekDBTPrint, \
    WeekDBTVertical, WeekNABView, WeekNABPrint, WeekNABVertical, WeekPPBView, WeekPPBPrint, WeekPPBVertical, WeekNBView, \
    WeekNBPrint, WeekNBVertical

urlpatterns = [
    path('', views.index, name='index'),
    path('novosti/', views.news, name='news'),
    path('novosti/<int:pk>/', views.news_view, name='news_view'),
    path('biblioteki/', views.biblioteki, name='biblioteki'),
    path('biblioteki/<int:pk>/', views.biblioteka, name='biblioteka'),
    path('categories/', views.document_categories, name='document_categories'),
    path('category/<int:category_id>/', views.documents_in_category, name='documents_in_category'),
    path('documents/', views.documents, name='documents'),
    path('documents/<int:pk>/', views.document, name='document'),
    path('polojenie/<int:pk>/', views.polojenie_view, name='polojenie'),
    path('services/', views.services, name='services'),
    path('quality/', views.raitings, name='raitings'),
    path('quality/<int:pk>/', views.raiting, name='raiting'),
    path('vacancy/', views.vacancies, name='vacancies'),
    path('vacancy/<int:pk>/', views.vacancy, name='vacancy'),
    path('fservices/<int:pk>/', views.free_services, name='free_services'),
    path('terms/<int:pk>/', views.termsofuse, name='termsofuse'),
    path('resources/', views.resources, name='resources'),
    path('projects/', views.projects_list, name='projects'),
    path('projects/<int:pk>/', views.project_view, name='project'),
    path('projects_other/', views.projects_other_list, name='projects_other'),
    path('projects_other/<int:pk>/', views.project_other_view, name='project_other'),
    path('articles/', views.articles_list, name='articles'),
    path('articles/<int:pk>/', views.article_view, name='article'),
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
    path('book-list/balashiha-golosa-serdetz/', views.library_balashiha, name='library_balashiha'),
    path('book-list/krai/', views.library_krai, name='library_krai'),
    path('book-list/hud/', views.library_hud, name='library_hud'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book_view'),
    path('events/', views.events, name='events'),
    path('events-archive/', views.events_archive, name='events_archive'),
    path('shedules/', views.shedules, name='shedules'),
    path('mobile-app/', views.mobile, name='mobile-app'),
    path('search/', views.search, name='search'),


    # """Schedules"""

    path('schedule_ikc/', WeekView.as_view(), name='schedule_ikc'),
    path('schedule-ikc-print/', WeekPrint.as_view(), name='schedule-ikc-print'),
    path('schedule-ikc-vertical/', WeekVertical.as_view(), name='schedule-ikc-vertical'),
    path('schedule_cdsch/', WeekCDSCHView.as_view(), name='schedule_cdsch'),
    path('schedule-cdsch-print/', WeekCDSCHPrint.as_view(), name='schedule-cdsch-print'),
    path('schedule-cdsch-vertical/', WeekCDSCHVertical.as_view(), name='schedule-cdsch-vertical'),
    path('schedule_ber/', WeekBERView.as_view(), name='schedule_ber'),
    path('schedule-ber-print/', WeekBERPrint.as_view(), name='schedule-ber-print'),
    path('schedule-ber-vertical/', WeekBERVertical.as_view(), name='schedule-ber-vertical'),
    path('schedule_f2/', WeekF2View.as_view(), name='schedule_f2'),
    path('schedule-f2-print/', WeekF2Print.as_view(), name='schedule-f2-print'),
    path('schedule-f2-vertical/', WeekF2Vertical.as_view(), name='schedule-f2-vertical'),
    path('schedule_f3/', WeekF3View.as_view(), name='schedule_f3'),
    path('schedule-f3-print/', WeekF3Print.as_view(), name='schedule-f3-print'),
    path('schedule-f3-vertical/', WeekF3Vertical.as_view(), name='schedule-f3-vertical'),
    path('schedule_f4/', WeekF4View.as_view(), name='schedule_f4'),
    path('schedule-f4-print/', WeekF4Print.as_view(), name='schedule-f4-print'),
    path('schedule-f4-vertical/', WeekF4Vertical.as_view(), name='schedule-f4-vertical'),
    path('schedule_b5/', WeekB5View.as_view(), name='schedule_b5'),
    path('schedule-b5-print/', WeekB5Print.as_view(), name='schedule-b5-print'),
    path('schedule-b5-vertical/', WeekB5Vertical.as_view(), name='schedule-b5-vertical'),
    path('schedule_cgbt/', WeekCGBTView.as_view(), name='schedule_cgbt'),
    path('schedule-cgbt-print/', WeekCGBTPrint.as_view(), name='schedule-cgbt-print'),
    path('schedule-cgbt-vertical/', WeekCGBTVertical.as_view(), name='schedule-cgbt-vertical'),
    path('schedule_bcj/', WeekBCJView.as_view(), name='schedule_bcj'),
    path('schedule-bcj-print/', WeekBCJPrint.as_view(), name='schedule-bcj-print'),
    path('schedule-bcj-vertical/', WeekBCJVertical.as_view(), name='schedule-bcj-vertical'),
    path('schedule_bscd/', WeekBSCDView.as_view(), name='schedule_bscd'),
    path('schedule-bscd-print/', WeekBSCDPrint.as_view(), name='schedule-bscd-print'),
    path('schedule-bscd-vertical/', WeekBSCDVertical.as_view(), name='schedule-bscd-vertical'),
    path('schedule_yb/', WeekYBView.as_view(), name='schedule_yb'),
    path('schedule-yb-print/', WeekYBPrint.as_view(), name='schedule-yb-print'),
    path('schedule-yb-vertical/', WeekYBVertical.as_view(), name='schedule-yb-vertical'),
    path('schedule_db/', WeekDBView.as_view(), name='schedule_db'),
    path('schedule-db-print/', WeekDBPrint.as_view(), name='schedule-db-print'),
    path('schedule-db-vertical/', WeekDBVertical.as_view(), name='schedule-db-vertical'),
    path('schedule_nmb/', WeekNMBView.as_view(), name='schedule_nmb'),
    path('schedule-nmb-print/', WeekNMBPrint.as_view(), name='schedule-nmb-print'),
    path('schedule-nmb-vertical/', WeekNMBVertical.as_view(), name='schedule-nmb-vertical'),
    path('schedule_csb/', WeekCSBView.as_view(), name='schedule_csb'),
    path('schedule-csb-print/', WeekCSBPrint.as_view(), name='schedule-csb-print'),
    path('schedule-csb-vertical/', WeekCSBVertical.as_view(), name='schedule-csb-vertical'),
    path('schedule_ssb/', WeekSSBView.as_view(), name='schedule_ssb'),
    path('schedule-ssb-print/', WeekSSBPrint.as_view(), name='schedule-ssb-print'),
    path('schedule-ssb-vertical/', WeekSSBVertical.as_view(), name='schedule-ssb-vertical'),
    path('schedule_fsb/', WeekFSBView.as_view(), name='schedule_fsb'),
    path('schedule-fsb-print/', WeekFSBPrint.as_view(), name='schedule-fsb-print'),
    path('schedule-fsb-vertical/', WeekFSBVertical.as_view(), name='schedule-fsb-vertical'),
    path('schedule_dbt/', WeekDBTView.as_view(), name='schedule_dbt'),
    path('schedule-dbt-print/', WeekDBTPrint.as_view(), name='schedule-dbt-print'),
    path('schedule-dbt-vertical/', WeekDBTVertical.as_view(), name='schedule-dbt-vertical'),
    path('schedule_nab/', WeekNABView.as_view(), name='schedule_nab'),
    path('schedule-nab-print/', WeekNABPrint.as_view(), name='schedule-nab-print'),
    path('schedule-nab-vertical/', WeekNABVertical.as_view(), name='schedule-nab-vertical'),
    path('schedule_ppb/', WeekPPBView.as_view(), name='schedule_ppb'),
    path('schedule-ppb-print/', WeekPPBPrint.as_view(), name='schedule-ppb-print'),
    path('schedule-ppb-vertical/', WeekPPBVertical.as_view(), name='schedule-ppb-vertical'),
    path('schedule_nb/', WeekNBView.as_view(), name='schedule_nb'),
    path('schedule-nb-print/', WeekNBPrint.as_view(), name='schedule-nb-print'),
    path('schedule-nb-vertical/', WeekNBVertical.as_view(), name='schedule-nb-vertical'),
    path('cinema/', CinemaWeekView.as_view(), name='cinema'),
    path('cinema-print/', CinemaWeekPrint.as_view(), name='cinema-print'),


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
