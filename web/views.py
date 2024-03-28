from django.views.generic import ListView
from rest_framework import generics
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.mail import send_mail
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import EmailMessage
from django.views.decorators.cache import cache_page
from datetime import datetime, timedelta

from .forms import *
from .models import *
import datetime
from django.views import generic, View
from .serializers import (BibliotekaSerializer, NewsSerializer,
                          EventySerializer, ServiceSerializer, BookFormSerializer, ActiveWeeksSerializer,
                          WeekSerializer, EventSerializer, WeekCDSCHSerializer, WeekBERSerializer, WeekF2Serializer,
                          WeekF3Serializer, WeekF4Serializer, CinemaWeekSerializer)


def getRoutes(request):
    routes = [
        {
            'Endpoint': '/books/create',
            'method': 'POST',
            'body': {'body': ""},
            'description': 'Новый запрос на продление книг'
        }
    ]
    return Response(routes)

@cache_page(60*10)
def index(request):
    title = 'МБУК ЦБС им. А. Белого'
    description = 'Официальный сайт Централизованной библиотечной сети имени Андрея Белого. Библиотека Железнодорожный'
    anonsy = Anons.objects.all().order_by('-id')
    categories = Category.objects.prefetch_related('news')
    category = Category.objects.all()
    datenow = date.today()
    event = Event.objects.filter(date__gt=datenow).order_by('date').first()
    cinema = Cinema.objects.latest('id')
    partners1 = Partner.objects.filter(block='1').order_by('?')
    partners2 = Partner.objects.filter(block='2').order_by('?')
    branch_categories = categories.get_descendants(include_self=True).select_related('news')
    news_list = News.objects.filter(category__in=branch_categories).distinct().order_by('-date')[:6]

    return render(request, 'index.html', {'title': title, 'description': description, 'anonsy': anonsy, 'news': news,
                                          'category': category, 'categories': categories, 'news_list': news_list,
                                          'partners1': partners1, 'partners2': partners2, 'event': event,
                                          'cinema': cinema})

@cache_page(60*15)
def biblioteki(request):
    title = 'Состав централизованной библиотечной системы'
    description = 'Состав централизованной библиотечной системы. Список библиотек в микрорайоне Железнодорожный'
    biblioteki = Biblioteka.objects.all()
    return render(request, 'biblioteki.html', {'title': title, 'biblioteki': biblioteki})

@cache_page(60*15)
def biblioteka(request, pk):
    biblioteka = get_object_or_404(Biblioteka, pk=pk)
    title = biblioteka.name
    description = biblioteka.description
    direktor = biblioteka.direktor
    phone = biblioteka.phone
    return render(request, 'biblioteka.html', {'title': title, 'biblioteka': biblioteka, 'direktor': direktor,
                                               'phone': phone, 'description': description})

@cache_page(60*15)
def news(request):
    categories = Category.objects.prefetch_related('news')
    title = 'Новости ЦБС им. А. Белого'
    description = 'Новости и события произошедшие в библиотеках Железнодорожного'
    branch_categories = categories.get_descendants(include_self=True)
    news_list = News.objects.filter(category__in=branch_categories).distinct().order_by('-date')
    paginator = Paginator(news_list, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)
    return render(request, 'news_all.html', {'categories': categories, 'title': title, 'paginator': paginator, 'page_obj': page_obj, 'description': description})

@cache_page(60*15)
def news_view(request, pk):
    news = get_object_or_404(News, pk=pk)
    category = Category.objects.prefetch_related('news')
    title = news.name
    image = news.image
    description = news.description
    date = news.date
    return render(request, 'news.html', {'news': news, 'title': title, 'image': image, 'description': description,
                                         'date': date, 'category': category})


def document_categories(request):
    # Список id категорий, которые вы хотите вывести
    category_ids = [14, 10, 16, 15]  # Пример списка id категорий

    # Запрос категорий по их id
    categories = Category.objects.filter(id__in=category_ids)
    return render(request, 'documents_category.html', {'categories': categories})


def documents_in_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    documents = Document.objects.filter(category=category, published=True)
    polojeniya = PolojenieKonkurs.objects.filter(category=category, published=True)

    # Объединение результатов запросов
    combined_results = list(documents) + list(polojeniya)
    combined_results.sort(key=lambda x: x.date, reverse=True)

    paginator = Paginator(combined_results, 10)  # Разбивка на страницы по 10 документов
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'page_obj': page_obj,
    }

    return render(request, 'documents.html', context)


@cache_page(60*15)
def documents(request):
    categories = Category.objects.prefetch_related('documents')
    title = 'Официальные документы библиотечной системы'
    description = 'Официальные документы МБУК ЦБС им. А. Белого'
    branch_categories = categories.get_descendants(include_self=True)
    docs_list = Document.objects.filter(category__in=branch_categories).distinct().order_by('-date')
    paginator = Paginator(docs_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'documents.html', {'categories': categories, 'title': title, 'docs_list': docs_list,
                                              'paginator': paginator, 'page_obj': page_obj, 'description': description})

@cache_page(60*15)
def document(request, pk):
    document = get_object_or_404(Document, pk=pk)
    category = document.category
    title = document.name
    image = document.image
    description = document.description
    date = document.date
    return render(request, 'document.html', {'title': title, 'document': document, 'date': date, 'description': description,
                                             'image': image, 'category': category})


def polojenie_view(request, pk):
    polojenie = get_object_or_404(PolojenieKonkurs, pk=pk)
    category = polojenie.category
    title = polojenie.name
    image = polojenie.image
    description = polojenie.description
    date = polojenie.date
    start_date = polojenie.date
    end_date = polojenie.date
    pdf = polojenie.konkurs_doc
    doc = polojenie.konkurs_zayavka
    return render(request, 'polojenie.html', {'title': title, 'polojenie': polojenie, 'date': date,
                                             'description': description, 'image': image, 'category': category,
                                             'start_date': start_date, 'end_date': end_date, 'pdf': pdf, 'doc': doc})


@cache_page(60*15)
def services(request):
    categories = Category.objects.prefetch_related('services')
    title = 'Услуги библиотечной системы'
    description = 'Список услуг предоставляемых в централизованной библиотечной системе. Услуги библиотек Железнодорожного'
    branch_categories = categories.get_descendants(include_self=True)
    services_list = Service.objects.filter(category__in=branch_categories).distinct().order_by('id')
    paginator = Paginator(services_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'services_all.html', {'categories': categories, 'title': title,
                                                 'services_list': services_list, 'paginator': paginator,
                                                 'page_obj': page_obj, 'description': description})

@cache_page(60*15)
def free_services(request, pk):
    fservice = get_object_or_404(FreeService, pk=pk)
    title = fservice.name
    description = fservice.description
    date = fservice.date
    return render(request, 'fservice.html', {'title': title, 'fservice': fservice, 'date': date,
                                             'description': description})

@cache_page(60*15)
def termsofuse(request, pk):
    tofuse = get_object_or_404(TermsOfUse, pk=pk)
    title = tofuse.name
    description = tofuse.description
    date = tofuse.date
    return render(request, 'termsofuse.html', {'title': title, 'tofuse': tofuse, 'date': date, 'description': description})

@cache_page(60*15)
def raitings(request):
    categories = Category.objects.prefetch_related('raitings')
    title = 'Документы оценки качества'
    branch_categories = categories.get_descendants(include_self=True)
    raitings = Raiting.objects.filter(category__in=branch_categories).distinct().order_by('-date')
    paginator = Paginator(raitings, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'qualitys.html', {'categories': categories, 'title': title, 'raitings': raitings,
                                             'paginator': paginator, 'page_obj': page_obj})

@cache_page(60*15)
def raiting(request, pk):
    quality = get_object_or_404(Raiting, pk=pk)
    title = quality.name
    date = quality.date
    name = quality.name
    description = quality.description
    return render(request, 'quality.html', {'title': title, 'date': date, 'name': name, 'description': description})

@cache_page(60*15)
def vacancies(request):
    title = 'Вакансии МБУК "ЦБС им. А. Белого'
    vacancies = Vacancy.objects.all()
    paginator = Paginator(vacancies, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'vacancies.html', {'title': title, 'vacancies': vacancies,
                                              'paginator': paginator, 'page_obj': page_obj})

@cache_page(60*15)
def vacancy(request, pk):
    vacancy = get_object_or_404(Vacancy, pk=pk)
    title = vacancy.name
    name = vacancy.name
    date = vacancy.date
    salary = vacancy.salary
    description = vacancy.description
    return render(request, 'vacancy.html', {'title': title, 'name': name, 'vacancy': vacancy, 'date': date, 'salary': salary,
                                            'description': description})

def contacts(request):
    title = 'Контакты'
    biblioteki = Biblioteka.objects.all()
    description = 'Контакты и способы связи с сотрудниками и руководством Библиотек Балашиха мкр Железнодорожный'

    if request.method == 'POST':
        fback = FeedbackForm(request.POST)

        if fback.is_valid():
            Feedback = fback.save(commit=False)
            Feedback.save()
            return redirect('/')

    else:
        fback = FeedbackForm()

    return render(request, 'contacts.html', {'fback': fback, 'title': title, 'biblioteki': biblioteki, 'description': description})


def resources(request):
    title = 'Данный раздел на данный момент не доступен'
    text = 'Раздел находится в процессе доработки и наполнения материалами. Попробуйте вернутся позже'
    return render(request, 'empty.html', {'title': title, 'text': text})

@cache_page(60*15)
def projects(request):
    title = 'Данный раздел на данный момент не доступен'
    text = 'Раздел находится в процессе доработки и наполнения материалами. Попробуйте вернутся позже'
    return render(request, 'empty.html', {'title': title, 'text': text})

@cache_page(60*15)
def veterany_vov(request):
    title = 'Жители Железнодорожного - участники Великой Отечественной войны'
    veterans = VeteranVOV.objects.all()
    paginator = Paginator(veterans, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'veterany_vov.html', {'title': title, 'veterans': veterans, 'paginator': paginator,
                                                 'page_obj': page_obj})

@cache_page(60*15)
def veterany_tyla(request):
    title = 'Труженики тыла'
    veterans = VeteranTruda.objects.all()
    return render(request, 'veterany_tyla.html', {'title': title, 'veterans': veterans})


def lg_residents(request):
    title = 'Жители блокадного Ленинграда, проживающие в Железнодорожном.'
    residents = LeningradResident.objects.all()
    return render(request, 'lg_residents_vov.html', {'title': title, 'residents': residents})


def kniga_pamyati(request):
    title = 'Книга памяти'
    heroes = HeroMemoryBook.objects.all()
    return render(request, 'vov_kniga_pamyati.html', {'title': title, 'heroes': heroes})


def book_form(request):
    title = 'Форма продления книг/и'
    sent = False
    if request.method == 'POST':
        bform = BookForm(request.POST)
        if bform.is_valid() and bform.cleaned_data['agreement']:
            Book = bform.save(commit=False)
            Book.save()
            return redirect('/')

    else:
        bform = BookForm()

    return render(request, 'book_form.html', {'title': title, 'bform': bform})


def q_form(request):
    title = 'Задайте ваш вопрос библиотекарю'
    sent = False
    if request.method == 'POST':
        qform = QuestionForm(request.POST)
        if qform.is_valid() and qform.cleaned_data['agreement']:
            Question = qform.save(commit=False)
            cd = qform.cleaned_data
            Question.save()
            subject = 'Вопрос библиотекарю от {} ({})'.format(cd['name'], cd['email'])
            message = '"{}". {}'.format(cd['comment'], cd['name'])
            send_mail(subject, message, 'site@obs-balashiha.ru', [cd['email'], 'bib76@biblioteka-belogo.ru'])
            sent = True
            return redirect('/')

    else:
        qform = QuestionForm()

    return render(request, 'q_form.html', {'title': title, 'qform': qform, 'sent': sent})


def brq_form(request):
    title = 'Комплектуем библиотеку вместе'
    sent = False
    if request.method == 'POST':
        brqform = BookrequestForm(request.POST)
        if brqform.is_valid() and brqform.cleaned_data['agreement']:
            Bookrequest = brqform.save(commit=False)
            Bookrequest.save()
            return redirect('/')

    else:
        brqform = BookrequestForm()

    return render(request, 'brq_form.html', {'title': title, 'brqform': brqform})


from django.core.exceptions import ValidationError


def s_form(request):
    title = 'Ваше мероприятие или аренда зала'
    sent = False
    if request.method == 'POST':
        sform = ServiceDopForm(request.POST, request.FILES)
        if sform.is_valid() and sform.cleaned_data['agreement']:
            ServiceDop = sform.save(commit=False)
            ServiceDop.save()
             # Отправка данных на email
            message = f"Дата: {ServiceDop.date}\nФИО: {ServiceDop.fio}\nНомер телефона: {ServiceDop.phone}\nЕ-мэйл: {ServiceDop.email}\nКомментарий: {ServiceDop.comment}"
            email = EmailMessage(
                'Новая форма дополнительной услуги',
                message,
                'site@obs-balashiha.ru',
                ['bib76@obs-balashiha.ru']
            )
             # Добавление файла вложением
            if request.FILES.get('file'):
                email.attach(request.FILES['file'].name, request.FILES['file'].read(), request.FILES['file'].content_type)
            email.send()
            return redirect('/')
    else:
        sform = ServiceDopForm()
    return render(request, 's_form.html', {'title': title, 'sform': sform})

@cache_page(60*15)
def library_category(request):
    title = 'Разделы электронной библиотеки'
    return render(request, 'library_category.html', {'title': title})


# @cache_page(60*15)
def library_balashiha(request):
    title = 'Журнал: "Балашиха: Голоса сердец"'
    categories = LibraryCategory.objects.filter(name='Журнал: "Балашиха: Голоса сердец"')
    books_list = Library.objects.filter(category__in=categories).distinct().order_by('id')
    paginator = Paginator(books_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'book_list.html', {'categories': categories, 'title': title,
                                             'books_list': books_list, 'paginator': paginator, 'page_obj': page_obj})

# @cache_page(60*15)
def library_imperia(request):
    title = 'Книги, изданные до 1917 года'
    categories = LibraryCategory.objects.filter(name='Книги, изданные до 1917 года')
    books_list = Library.objects.filter(category__in=categories).distinct().order_by('id')
    paginator = Paginator(books_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'book_list.html', {'categories': categories, 'title': title,
                                             'books_list': books_list, 'paginator': paginator, 'page_obj': page_obj})

# @cache_page(60*15)
def library_krai(request):
    title = 'Краеведческая литература'
    categories = LibraryCategory.objects.filter(name='Краеведческая литература')
    books_list = Library.objects.filter(category__in=categories).distinct().order_by('id')
    paginator = Paginator(books_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'book_list.html', {'categories': categories, 'title': title,
                                             'books_list': books_list, 'paginator': paginator, 'page_obj': page_obj})

# @cache_page(60*15)
def library_hud(request):
    title = 'Художественная литература'
    categories = LibraryCategory.objects.filter(name='Художественная литература')
    books_list = Library.objects.filter(category__in=categories).distinct().order_by('id')
    paginator = Paginator(books_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'book_list.html', {'categories': categories, 'title': title, 'books_list': books_list,
                                              'paginator': paginator, 'page_obj': page_obj})



class BookDetailView(generic.DetailView):
    model = Library
    template_name = 'book_view.html'
    context_object_name = 'book'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Проверяем, существует ли уже запись о просмотре книги сегодня
        today_views = BookView.objects.filter(book=self.object, viewed_at=timezone.now().date())
        if today_views.exists():
            # Если запись сегодняшнего просмотра уже существует, увеличиваем счетчик
            today_view = today_views.first()
            today_view.view_count += 1
            today_view.save()
        else:
            # Если запись сегодняшнего просмотра еще не существует, создаем новую
            BookView.objects.create(book=self.object)
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return get_object_or_404(Library, pk=self.kwargs.get('pk'))


@cache_page(60*10)
def events(request):
    title = 'Мероприятия и события'
    description = 'Ожидаемые и недавно прошедшие мероприятия и события в библиотеках Балашихи в микрорайоне Железнодорожный'
    events = Event.objects.all()

    for event in events:
        event.date_iso = event.date.isoformat()
        if event.date_end:
            event.date_end_iso = event.date_end.isoformat()
        else:
            event.date_end_iso = None

    context = {'title': title, 'description': description, 'events': events}
    return render(request, 'events.html', context)


@cache_page(60*15)
def shedules(request):
    title = 'Системные расписания'
    description = 'Системные библиотек "ЦБС им. А. Белого"'
    schedule_ikc = Week.objects.filter(active=True)
    schedule_cdsch = WeekCDSCH.objects.filter(active=True)
    schedule_ber = WeekBER.objects.filter(active=True)
    schedule_f2 = WeekF2.objects.filter(active=True)
    schedule_f3 = WeekF3.objects.filter(active=True)
    schedule_f4 = WeekF4.objects.filter(active=True)
    return render(request, 'shedules.html', {'title': title, 'description': description, 'schedule_ikc': schedule_ikc,
                                             'schedule_cdsch':schedule_cdsch, 'schedule_ber':schedule_ber,
                                             'schedule_f2':schedule_f2, 'schedule_f3':schedule_f3,
                                             'schedule_f4':schedule_f4})


@cache_page(60*15)
def events_archive(request):
    title = 'Архив мероприятий'
    description = 'Архив прошедших в билиотеках Балашихи мероприятий'
    events = Event.objects.order_by('-date')
    datenow = datetime.date.today()
    closest_event_date = None

    for event in events:
        event.date_iso = event.date.isoformat()
    paginator = Paginator(events, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'events': events, 'title': title, 'paginator': paginator, 'page_obj': page_obj,
               'description': description, 'datenow': datenow, 'closest_event_date': closest_event_date}
    return render(request, 'events_archive.html', context)

def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)


class BibliotekiAPIView(generics.ListAPIView):
    queryset = Biblioteka.objects.order_by('id')
    serializer_class = BibliotekaSerializer


class NewsAPIView(generics.ListAPIView):
    queryset = News.objects.order_by('-id')[0:20]
    serializer_class = NewsSerializer


class EventAPIView(generics.ListAPIView):
    queryset = Event.objects.order_by('-id')[0:30]
    serializer_class = EventSerializer


class ServiceAPIView(generics.ListAPIView):
    queryset = Service.objects.order_by('id')
    serializer_class = ServiceSerializer


@api_view(['POST'])
def createBook(request):
    data = request.data

    book = Book.objects.create(
        library=data['library'],
        fio=data['fio'],
        bilet=data['bilet'],
        email=data['email'],
        comment=data['comment']
    )
    serializer = BookFormSerializer(book, many=False)
    return Response(serializer.data)


class CinemaWeekView(ListView):
    model = CinemaWeek
    template_name = 'cinema.html'  # Replace 'week.html' with the actual template name
    def get_queryset(self):
        return CinemaWeek.objects.filter(active=True)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cinemadays'] = CinemaDay.objects.filter(cinemaweek__active=True)
        return context


class WeekView(ListView):
    model = Week
    template_name = 'schedule_ikc.html'  # Replace 'week.html' with the actual template name

    def get_queryset(self):
        return Week.objects.filter(active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['weekdays'] = Day.objects.filter(week__active=True)
        context['start_date'] = self.get_queryset().first().start_date
        context['end_date'] = self.get_queryset().first().end_date
        context['biblioteka'] = Biblioteka.objects.get(id=1)
        return context


class WeekCDSCHView(ListView):
    model = WeekCDSCH
    template_name = 'schedule_cdsch.html'

    def get_queryset(self):
        return WeekCDSCH.objects.filter(active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['weekdays'] = DayCDSCH.objects.filter(week__active=True)
        context['start_date'] = self.get_queryset().first().start_date
        context['end_date'] = self.get_queryset().first().end_date
        context['biblioteka'] = Biblioteka.objects.get(id=2)
        return context


class WeekBERView(ListView):
    model = WeekBER
    template_name = 'schedule_ber.html'

    def get_queryset(self):
        return WeekBER.objects.filter(active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['weekdays'] = DayBER.objects.filter(week__active=True)
        context['start_date'] = self.get_queryset().first().start_date
        context['end_date'] = self.get_queryset().first().end_date
        context['biblioteka'] = Biblioteka.objects.get(id=3)
        return context


class WeekF2View(ListView):
    model = WeekF2
    template_name = 'schedule_f2.html'

    def get_queryset(self):
        return WeekF2.objects.filter(active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['weekdays'] = DayF2.objects.filter(week__active=True)
        context['start_date'] = self.get_queryset().first().start_date
        context['end_date'] = self.get_queryset().first().end_date
        context['biblioteka'] = Biblioteka.objects.get(id=4)
        return context


class WeekF3View(ListView):
    model = WeekF3
    template_name = 'schedule_f3.html'

    def get_queryset(self):
        return WeekF3.objects.filter(active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['weekdays'] = DayF3.objects.filter(week__active=True)
        context['start_date'] = self.get_queryset().first().start_date
        context['end_date'] = self.get_queryset().first().end_date
        context['biblioteka'] = Biblioteka.objects.get(id=5)
        return context


class WeekF4View(ListView):
    model = WeekF4
    template_name = 'schedule_f4.html'

    def get_queryset(self):
        return WeekF4.objects.filter(active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['weekdays'] = DayF4.objects.filter(week__active=True)
        context['start_date'] = self.get_queryset().first().start_date
        context['end_date'] = self.get_queryset().first().end_date
        context['biblioteka'] = Biblioteka.objects.get(id=6)
        return context


class ActiveWeeksAPIView(APIView):
    def get(self, request):
        weeks = []

        # Блок 1
        queryset_week = Week.objects.filter(active=True)
        title_week = Week._meta.verbose_name
        serializer_week = WeekSerializer(queryset_week, many=True)
        weeks.extend(self.add_title(serializer_week.data, title_week))

        # Блок 2
        queryset_week_cdsch = WeekCDSCH.objects.filter(active=True)
        title_week_cdsch = WeekCDSCH._meta.verbose_name
        serializer_week_cdsch = WeekCDSCHSerializer(queryset_week_cdsch, many=True)
        weeks.extend(self.add_title(serializer_week_cdsch.data, title_week_cdsch))

        # Блок 3
        queryset_week_ber = WeekBER.objects.filter(active=True)
        title_week_ber = WeekBER._meta.verbose_name
        serializer_week_ber = WeekBERSerializer(queryset_week_ber, many=True)
        weeks.extend(self.add_title(serializer_week_ber.data, title_week_ber))

        # Блок 4
        queryset_week_f2 = WeekF2.objects.filter(active=True)
        title_week_f2 = WeekF2._meta.verbose_name
        serializer_week_f2 = WeekF2Serializer(queryset_week_f2, many=True)
        weeks.extend(self.add_title(serializer_week_f2.data, title_week_f2))

        # Блок 5
        queryset_week_f3 = WeekF3.objects.filter(active=True)
        title_week_f3 = WeekF3._meta.verbose_name
        serializer_week_f3 = WeekF3Serializer(queryset_week_f3, many=True)
        weeks.extend(self.add_title(serializer_week_f3.data, title_week_f3))

        # Блок 6
        queryset_week_f4 = WeekF4.objects.filter(active=True)
        title_week_f4 = WeekF4._meta.verbose_name
        serializer_week_f4 = WeekF4Serializer(queryset_week_f4, many=True)
        weeks.extend(self.add_title(serializer_week_f4.data, title_week_f4))

        return Response(weeks)

    def add_title(self, data, title):
        return [{'title': title, 'data': data}]


class WeekAPIView(APIView):
    def get(self, request):
        queryset = Week.objects.filter(active=True)
        serializer = WeekSerializer(queryset, many=True)
        return Response(serializer.data)


class CinemaWeekAPIView(APIView):
    def get(self, request):
        queryset = CinemaWeek.objects.filter(active=True)
        serializer = CinemaWeekSerializer(queryset, many=True)
        return Response(serializer.data)


def mobile(request):
    title = 'Скачать мобильное приложение'
    description = 'Мобильное приложение МБУК "ЦБС им. А. Белого" - БИБЛИОТЕКА В КАРМАНЕ'
    return render(request, 'mobile.html', {'title': title, 'description': description})


class WeekPrint(ListView):
    model = Week
    template_name = 'schedule_ikc.html'

    def get_queryset(self):
        active_week = Week.objects.get(active=True)
        next_week_start_date = active_week.end_date + timedelta(days=1)
        return Week.objects.filter(start_date=next_week_start_date)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_week = Week.objects.get(active=True)
        next_week_start_date = active_week.end_date + timedelta(days=1)
        context['weekdays'] = Day.objects.filter(week__start_date=next_week_start_date)
        context['start_date'] = next_week_start_date
        context['end_date'] = next_week_start_date + timedelta(days=6)
        context['biblioteka'] = Biblioteka.objects.get(id=1)
        return context


class WeekVertical(ListView):
    model = Week
    template_name = 'schedule_ikc_vertical.html'

    def get_queryset(self):
        active_week = Week.objects.get(active=True)
        next_week_start_date = active_week.end_date + timedelta(days=1)
        return Week.objects.filter(start_date=next_week_start_date)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_week = Week.objects.get(active=True)
        next_week_start_date = active_week.end_date + timedelta(days=1)
        context['weekdays'] = Day.objects.filter(week__start_date=next_week_start_date)
        context['start_date'] = next_week_start_date
        context['end_date'] = next_week_start_date + timedelta(days=6)
        context['biblioteka'] = Biblioteka.objects.get(id=1)
        return context


class WeekCDSCHPrint(ListView):
    model = WeekCDSCH
    template_name = 'schedule_cdsch.html'

    def get_queryset(self):
        active_week = WeekCDSCH.objects.get(active=True)
        next_week_start_date = active_week.end_date + timedelta(days=1)
        return WeekCDSCH.objects.filter(start_date=next_week_start_date)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_week = WeekCDSCH.objects.get(active=True)
        next_week_start_date = active_week.end_date + timedelta(days=1)
        context['weekdays'] = DayCDSCH.objects.filter(week__start_date=next_week_start_date)
        context['start_date'] = next_week_start_date
        context['end_date'] = next_week_start_date + timedelta(days=6)
        context['biblioteka'] = Biblioteka.objects.get(id=2)
        return context


class WeekCDSCHVertical(ListView):
    model = WeekCDSCH
    template_name = 'schedule_cdsch_vertical.html'

    def get_queryset(self):
        active_week = WeekCDSCH.objects.get(active=True)
        next_week_start_date = active_week.end_date + timedelta(days=1)
        return WeekCDSCH.objects.filter(start_date=next_week_start_date)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_week = WeekCDSCH.objects.get(active=True)
        next_week_start_date = active_week.end_date + timedelta(days=1)
        context['weekdays'] = DayCDSCH.objects.filter(week__start_date=next_week_start_date)
        context['start_date'] = next_week_start_date
        context['end_date'] = next_week_start_date + timedelta(days=6)
        context['biblioteka'] = Biblioteka.objects.get(id=2)
        return context


class WeekBERPrint(ListView):
    model = WeekBER
    template_name = 'schedule_ber.html'

    def get_queryset(self):
        active_week = WeekBER.objects.get(active=True)
        next_week_start_date = active_week.end_date + timedelta(days=1)
        return WeekBER.objects.filter(start_date=next_week_start_date)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_week = WeekBER.objects.get(active=True)
        next_week_start_date = active_week.end_date + timedelta(days=1)
        context['weekdays'] = DayBER.objects.filter(week__start_date=next_week_start_date)
        context['start_date'] = next_week_start_date
        context['end_date'] = next_week_start_date + timedelta(days=6)
        context['biblioteka'] = Biblioteka.objects.get(id=3)
        return context


class WeekBERVertical(ListView):
    model = WeekBER
    template_name = 'schedule_ber_vertical.html'

    def get_queryset(self):
        active_week = WeekBER.objects.get(active=True)
        next_week_start_date = active_week.end_date + timedelta(days=1)
        return WeekBER.objects.filter(start_date=next_week_start_date)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_week = WeekBER.objects.get(active=True)
        next_week_start_date = active_week.end_date + timedelta(days=1)
        context['weekdays'] = DayBER.objects.filter(week__start_date=next_week_start_date)
        context['start_date'] = next_week_start_date
        context['end_date'] = next_week_start_date + timedelta(days=6)
        context['biblioteka'] = Biblioteka.objects.get(id=3)
        return context


class WeekF2Print(ListView):
    model = WeekF2
    template_name = 'schedule_f2.html'

    def get_queryset(self):
        active_week = WeekF2.objects.get(active=True)
        next_week_start_date = active_week.end_date + timedelta(days=1)
        return WeekF2.objects.filter(start_date=next_week_start_date)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_week = WeekF2.objects.get(active=True)
        next_week_start_date = active_week.end_date + timedelta(days=1)
        context['weekdays'] = DayF2.objects.filter(week__start_date=next_week_start_date)
        context['start_date'] = next_week_start_date
        context['end_date'] = next_week_start_date + timedelta(days=6)
        context['biblioteka'] = Biblioteka.objects.get(id=4)
        return context


class WeekF2Vertical(ListView):
    model = WeekF2
    template_name = 'schedule_f2_vertical.html'

    def get_queryset(self):
        active_week = WeekF2.objects.get(active=True)
        next_week_start_date = active_week.end_date + timedelta(days=1)
        return WeekF2.objects.filter(start_date=next_week_start_date)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_week = WeekF2.objects.get(active=True)
        next_week_start_date = active_week.end_date + timedelta(days=1)
        context['weekdays'] = DayF2.objects.filter(week__start_date=next_week_start_date)
        context['start_date'] = next_week_start_date
        context['end_date'] = next_week_start_date + timedelta(days=6)
        context['biblioteka'] = Biblioteka.objects.get(id=4)
        return context


class WeekF3Print(ListView):
    model = WeekF3
    template_name = 'schedule_f3.html'

    def get_queryset(self):
        active_week = WeekF3.objects.get(active=True)
        next_week_start_date = active_week.end_date + timedelta(days=1)
        return WeekF3.objects.filter(start_date=next_week_start_date)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_week = WeekF3.objects.get(active=True)
        next_week_start_date = active_week.end_date + timedelta(days=1)
        context['weekdays'] = DayF3.objects.filter(week__start_date=next_week_start_date)
        context['start_date'] = next_week_start_date
        context['end_date'] = next_week_start_date + timedelta(days=6)
        context['biblioteka'] = Biblioteka.objects.get(id=5)
        return context


class WeekF3Vertical(ListView):
    model = WeekF3
    template_name = 'schedule_f3_vertical.html'

    def get_queryset(self):
        active_week = WeekF3.objects.get(active=True)
        next_week_start_date = active_week.end_date + timedelta(days=1)
        return WeekF3.objects.filter(start_date=next_week_start_date)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_week = WeekF3.objects.get(active=True)
        next_week_start_date = active_week.end_date + timedelta(days=1)
        context['weekdays'] = DayF3.objects.filter(week__start_date=next_week_start_date)
        context['start_date'] = next_week_start_date
        context['end_date'] = next_week_start_date + timedelta(days=6)
        context['biblioteka'] = Biblioteka.objects.get(id=5)
        return context


class WeekF4Print(ListView):
    model = WeekF4
    template_name = 'schedule_f4.html'

    def get_queryset(self):
        active_week = WeekF4.objects.get(active=True)
        next_week_start_date = active_week.end_date + timedelta(days=1)
        return WeekF4.objects.filter(start_date=next_week_start_date)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_week = WeekF4.objects.get(active=True)
        next_week_start_date = active_week.end_date + timedelta(days=1)
        context['weekdays'] = DayF4.objects.filter(week__start_date=next_week_start_date)
        context['start_date'] = next_week_start_date
        context['end_date'] = next_week_start_date + timedelta(days=6)
        context['biblioteka'] = Biblioteka.objects.get(id=6)
        return context


class WeekF4Vertical(ListView):
    model = WeekF4
    template_name = 'schedule_f4_vertical.html'

    def get_queryset(self):
        active_week = WeekF4.objects.get(active=True)
        next_week_start_date = active_week.end_date + timedelta(days=1)
        return WeekF4.objects.filter(start_date=next_week_start_date)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_week = WeekF4.objects.get(active=True)
        next_week_start_date = active_week.end_date + timedelta(days=1)
        context['weekdays'] = DayF4.objects.filter(week__start_date=next_week_start_date)
        context['start_date'] = next_week_start_date
        context['end_date'] = next_week_start_date + timedelta(days=6)
        context['biblioteka'] = Biblioteka.objects.get(id=6)
        return context


class CinemaWeekPrint(ListView):
    model = CinemaWeek
    template_name = 'cinema.html'  # Replace 'week.html' with the actual template name
    def get_queryset(self):
        active_week = CinemaWeek.objects.get(active=True)
        next_week_start_date = active_week.end_date + timedelta(days=1)
        return CinemaWeek.objects.filter(start_date=next_week_start_date)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cinemadays'] = CinemaDay.objects.filter(cinemaweek__active=True)
        return context





