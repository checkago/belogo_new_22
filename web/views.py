from rest_framework import generics
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.core.mail import send_mail
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .forms import *
from .models import *
import datetime
from django.views import generic
from .serializers import BibliotekaSerializer, NewsSerializer, EventSerializer, SheduleSerializer, ServiceSerializer, \
    BookFormSerializer


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


def index(request):
    title = 'МБУК ЦБС им. А. Белого'
    description = 'Официальный сайт Централизованной библиотечной сети имени Андрея Белого. Библиотека Железнодорожный'
    anonsy = Anons.objects.all().order_by('-id')
    categories = Category.objects.filter(name='Новости')
    category = Category.objects.all()
    shedule = Shedule.objects.first()
    event = Event.objects.latest('id')
    cinema = Cinema.objects.latest('id')
    partners1 = Partner.objects.filter(block='1').order_by('?')
    partners2 = Partner.objects.filter(block='2').order_by('?')
    branch_categories = categories.get_descendants(include_self=True)
    news_list = News.objects.filter(category__in=branch_categories).distinct().order_by('-date')[:6]

    return render(request, 'index.html', {'title': title, 'description': description, 'anonsy': anonsy, 'news': news,
                                          'category': category, 'categories': categories, 'news_list': news_list,
                                          'partners1': partners1, 'partners2': partners2, 'shedule': shedule,
                                          'event': event, 'cinema': cinema})


def biblioteki(request):
    title = 'Состав централизованной библиотечной системы'
    description = 'Состав централизованной библиотечной системы. Список библиотек в микрорайоне Железнодорожный'
    biblioteki = Biblioteka.objects.all()
    return render(request, 'biblioteki.html', {'title': title, 'biblioteki': biblioteki})


def biblioteka(request, pk):
    biblioteka = get_object_or_404(Biblioteka, pk=pk)
    title = biblioteka.name
    description = biblioteka.description
    direktor = Biblioteka.direktor
    phone = Biblioteka.phone
    return render(request, 'biblioteka.html', {'title': title, 'biblioteka': biblioteka, 'direktor': direktor,
                                               'phone': phone, 'description': description})


def news(request):
    categories = Category.objects.filter(name='Новости')
    title = 'Новости ЦБС им. А. Белого'
    description = 'Новости и события произошедшие в библиотеках Железнодорожного'
    branch_categories = categories.get_descendants(include_self=True)
    news_list = News.objects.filter(category__in=branch_categories).distinct().order_by('-date')
    paginator = Paginator(news_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'news_all.html', {'categories': categories, 'title': title, 'news_list': news_list,
                                             'paginator': paginator, 'page_obj': page_obj, 'description': description})


def news_view(request, pk):
    news = get_object_or_404(News, pk=pk)
    category = Category.objects.filter(name='Новости')
    title = news.name
    image = News.image
    description = news.description
    date = News.date
    return render(request, 'news.html', {'news': news, 'title': title, 'image': image, 'description': description,
                                         'date': date, 'category': category})


def documents(request):
    categories = Category.objects.filter(name='Документы')
    title = 'Официальные документы библиотечной системы'
    description = 'Официальные документы МБУК ЦБС им. А. Белого'
    branch_categories = categories.get_descendants(include_self=True)
    docs_list = Document.objects.filter(category__in=branch_categories).distinct().order_by('-date')
    paginator = Paginator(docs_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'documents.html', {'categories': categories, 'title': title, 'docs_list': docs_list,
                                              'paginator': paginator, 'page_obj': page_obj, 'description': description})


def document(request, pk):
    document = get_object_or_404(Document, pk=pk)
    category = Document.category
    title = document.name
    image = Document.image
    description = Document.description
    date = Document.date
    return render(request, 'document.html', {'title': title, 'document': document, 'date': date, 'description': description,
                                             'image': image, 'category': category})


def services(request):
    categories = Category.objects.filter(name='Услуги')
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


def free_services(request, pk):
    fservice = get_object_or_404(FreeService, pk=pk)
    title = fservice.name
    description = fservice.description
    date = fservice.date
    return render(request, 'fservice.html', {'title': title, 'fservice': fservice, 'date': date,
                                             'description': description})


def termsofuse(request, pk):
    tofuse = get_object_or_404(TermsOfUse, pk=pk)
    title = tofuse.name
    description = tofuse.description
    date = tofuse.date
    return render(request, 'termsofuse.html', {'title': title, 'tofuse': tofuse, 'date': date, 'description': description})


def raitings(request):
    categories = Category.objects.filter(name='Оценка качества')
    title = 'Документы оценки качества'
    branch_categories = categories.get_descendants(include_self=True)
    raitings = Raiting.objects.filter(category__in=branch_categories).distinct().order_by('-date')
    paginator = Paginator(raitings, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'qualitys.html', {'categories': categories, 'title': title, 'raitings': raitings,
                                             'paginator': paginator, 'page_obj': page_obj})


def raiting(request, pk):
    quality = get_object_or_404(Raiting, pk=pk)
    title = quality.name
    date = quality.date
    name = quality.name
    description = quality.description
    return render(request, 'quality.html', {'title': title, 'date': date, 'name': name, 'description': description})


def vacancies(request):
    title = 'Вакансии МБУК "ЦБС им. А. Белого'
    vacancies = Vacancy.objects.all()
    paginator = Paginator(vacancies, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'vacancies.html', {'title': title, 'vacancies': vacancies,
                                              'paginator': paginator, 'page_obj': page_obj})


def vacancy(request, pk):
    vacancy = get_object_or_404(Vacancy, pk=pk)
    title = vacancy.name
    name = Vacancy.name
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
        fback = FeedbackForm(request.POST, initial={"category": "category"})

        if fback.is_valid():
            Feedback = fback.save(commit=False)
            cd = fback.cleaned_data
            Feedback.save()
            subject = 'Сообщение от {} ({})'.format(cd['name'], cd['email'])
            message = '"{}". {} | {}'.format(cd['comment'], cd['name'], cd['phone'])
            send_mail(subject, message, 'site@biblioteka-belogo.ru', [cd['email'], 'bib76@yandex.ru'])
            sent = True
            return redirect('/contacts')

    else:
        fback = FeedbackForm()

    return render(request, 'contacts.html', {'fback': fback, 'title': title, 'biblioteki': biblioteki, 'description': description})


def resources(request):
    title = 'Данный раздел на данный момент не доступен'
    text = 'Раздел находится в процессе доработки и наполнения материалами. Попробуйте вернутся позже'
    return render(request, 'empty.html', {'title': title, 'text': text})


def projects(request):
    title = 'Данный раздел на данный момент не доступен'
    text = 'Раздел находится в процессе доработки и наполнения материалами. Попробуйте вернутся позже'
    return render(request, 'empty.html', {'title': title, 'text': text})


def veterany_vov(request):
    title = 'Жители Железнодорожного - участники Великой Отечественной войны'
    veterans = VeteranVOV.objects.all()
    paginator = Paginator(veterans, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'veterany_vov.html', {'title': title, 'veterans': veterans, 'paginator': paginator,
                                                 'page_obj': page_obj})


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
    title = 'Форма форма продления книг/и'
    sent = False
    if request.method == 'POST':
        bform = BookForm(request.POST)
        if bform.is_valid():
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
        if qform.is_valid():
            Question = qform.save(commit=False)
            cd = qform.cleaned_data
            Question.save()
            subject = 'Вопрос библиотекарю от {} ({})'.format(cd['name'], cd['email'])
            message = '"{}". {}'.format(cd['comment'], cd['name'])
            send_mail(subject, message, 'site@biblioteka-belogo.ru', [cd['email'], 'bib76@yandex.ru'])
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
        if brqform.is_valid():
            Bookrequest = brqform.save(commit=False)
            Bookrequest.save()
            return redirect('/')

    else:
        brqform = BookrequestForm()

    return render(request, 'brq_form.html', {'title': title, 'brqform': brqform})


def s_form(request):
    title = 'Ваше мероприятие или аренда зала'
    sent = False
    if request.method == 'POST':
        sform = ServiceDopForm(request.POST)
        if sform.is_valid():
            ServiceDop = sform.save(commit=False)
            cd = sform.cleaned_data
            ServiceDop.save()
            subject = 'Запрос на "{}" от {} ({})'.format(cd['service'], cd['fio'], cd['email'])
            message = '{} "{}". {} | {}'.format(cd['service'], cd['comment'], cd['fio'], cd['phone'])
            send_mail(subject, message, 'site@biblioteka-belogo.ru', [cd['email'], 'bib76@yandex.ru'])
            sent = True
            return redirect('/')

    else:
        sform = ServiceDopForm()

    return render(request, 's_form.html', {'title': title, 'sform': sform, 'sent': sent})


def library_category(request):
    title = 'Разделы электронной библиотеки'
    return render(request, 'library_category.html', {'title': title})


def library_imperia(request):
    title = 'Книги, изданные до 1917 года'
    categories = LibraryCategory.objects.filter(name='Книги, изданные до 1917 года')
    books_list = Library.objects.filter(category__in=categories).distinct().order_by('id')
    paginator = Paginator(books_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'book_list.html', {'categories': categories, 'title': title,
                                             'books_list': books_list, 'paginator': paginator, 'page_obj': page_obj})


def library_krai(request):
    title = 'Краеведческая литература'
    categories = LibraryCategory.objects.filter(name='Краеведческая литература')
    books_list = Library.objects.filter(category__in=categories).distinct().order_by('id')
    paginator = Paginator(books_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'book_list.html', {'categories': categories, 'title': title,
                                             'books_list': books_list, 'paginator': paginator, 'page_obj': page_obj})


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
    title = Library.title
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Library.title
        context['author'] = Library.author
        context['image'] = Library.image
        context['description'] = Library.description
        context['link'] = Library.link
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.views += 1
        self.object.save()
        context = self.get_context_data(object=self.object, title=self.object.title)
        return self.render_to_response(context)


def events(request):
    title = 'Мероприятия и события'
    description = 'Ожидаемые и недавно прошедшие мероприятия и события в библиотеках Балашихи в микрорайоне Железнодорожный'
    events = Event.objects.order_by('-id')[:9]
    datenow = datetime.date.today()
    return render(request, 'events.html', {'title': title, 'description': description, 'events': events,
                                           'datenow': datenow})


def shedules(request):
    title = 'Системные расписания'
    description = 'Системные библиотек "ЦБС им. А. Белого"'
    shedules = Shedule.objects.order_by('id')
    return render(request, 'shedules.html', {'title': title, 'description': description, 'shedules': shedules})


def events_archive(request):
    title = 'Архив мероприятий'
    description = 'Архив прошедших в билиотеках Балашихи мероприятий'
    events = Event.objects.order_by('-id')
    datenow = datetime.date.today()
    paginator = Paginator(events, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'events_archive.html', {'events': events, 'title': title, 'paginator': paginator,
                                              'page_obj': page_obj, 'description': description, 'datenow': datenow})


def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)


class BibliotekiAPIView(generics.ListAPIView):
    queryset = Biblioteka.objects.all()
    serializer_class = BibliotekaSerializer


class NewsAPIView(generics.ListAPIView):
    queryset = News.objects.order_by("-id")[0:20]
    serializer_class = NewsSerializer


class EventAPIView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class SheduleAPIView(generics.ListAPIView):
    queryset = Shedule.objects.all()
    serializer_class = SheduleSerializer


class ServiceAPIView(generics.ListAPIView):
    queryset = Service.objects.all()
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
