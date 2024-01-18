from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from datetime import date

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from email_signals.models import EmailSignalMixin
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.safestring import mark_safe


from utils import upload_function


class Position(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название должности')

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'

    def __str__(self):
        return self.name


class Employers(models.Model):
    position = models.ForeignKey(Position, blank=True, on_delete=models.SET_NULL, related_name='employer', null=True, verbose_name='Должность')
    lastname = models.CharField(max_length=50, verbose_name='Фамилия')
    firstname = models.CharField(max_length=50, verbose_name='Имя')
    surname = models.CharField(max_length=50, verbose_name='Отчество')

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return format(self.lastname +' '+ self.firstname +' '+ self.surname)


class Category(MPTTModel):
    name = models.CharField(max_length=50, unique=True, verbose_name='Категория')
    slug = models.SlugField(max_length=128, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def get_pages(self):
        ids = self.get_descendants(include_self=True).values_list('id')
        return Book.objects.filter(category_id__in=ids).count()

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    class MPTTMeta:
        verbose_name = 'Категория'
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class Biblioteka(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(null=True, unique=True, verbose_name='Псевдоним')
    category = models.ForeignKey(Category, blank=True, on_delete=models.SET_NULL, null=True, verbose_name='Категория')
    phone = models.CharField(max_length=18, default='+7 (495) 555-55-55', verbose_name='Телефон')
    email = models.EmailField(verbose_name='Емэйл', blank=True)
    direktor = models.ForeignKey(u'Position', blank=True, on_delete=models.SET_NULL, related_name='positions', null=True, verbose_name='Должность')
    employer = models.ForeignKey(u'Employers', blank=True, on_delete=models.SET_NULL, related_name='employer', null=True, verbose_name='Руководитель')
    facebook = models.URLField(verbose_name='страница в ВКонтакте', blank=True, null=True)
    instagram = models.URLField(verbose_name='страница в Одноклассниках', blank=True, null=True)
    telegram = models.URLField(verbose_name='аккаунт Телеграмм', blank=True, null=True)
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='img/cbs', blank=True, null=True, verbose_name='Фото')
    worktime = models.CharField(max_length=50, verbose_name='Время работы', blank=True, default='09:00 - 21:00')
    workdays = models.CharField(max_length=50, verbose_name='Рабочие дни', blank=True, default='Понедельник-Пятница')
    worktime_alt = models.CharField(max_length=50, verbose_name='Время работы', blank=True, default='09:00 - 21:00')
    workdays_alt = models.CharField(max_length=50, verbose_name='Рабочие дни', blank=True, default='Суббота-Воскресенье')
    weekend = models.CharField(max_length=50, verbose_name='Выходной', blank=True, default='Воскресенье')
    adress = models.CharField(max_length=250, verbose_name='Адрес')
    primary = models.BooleanField(default=False, verbose_name='Основное подразделение')
    map = models.URLField(blank=True, null=True, verbose_name='Ссылка на карту')

    class Meta:
        verbose_name = 'Библиотека/Филиал'
        verbose_name_plural = 'Библиотеки/Филиалы'

    def __str__(self):
        return self.name


class ImageGallery(models.Model):

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    image = models.ImageField(upload_to=upload_function)

    class Meta:
        verbose_name = 'Галерея изображений'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"Изображение для {self.content_object}"

    def image_url(self):
        return mark_safe(f'<img src="{self.image.url}" width="auto" height="100px"')


class News(models.Model):
    date = models.DateField(default=date.today, verbose_name='Дата')
    name = models.CharField(max_length=250, verbose_name='Заголовок', db_index=True)
    slug = models.SlugField(null=True, unique=True, verbose_name='Псевдоним')
    category = models.ForeignKey(Category, blank=True, on_delete=models.SET_NULL, related_name='news', null=True,
                                 verbose_name='Категория', db_index=True)
    description = models.TextField(verbose_name='Текст')
    image = models.ImageField(upload_to='img/news', blank=True, null=True, verbose_name='Главное фото')
    published = models.BooleanField(default=True, verbose_name='Опубликована')
    image_gallery = GenericRelation('imagegallery')

    class Meta:
        default_related_name = 'news'
        verbose_name = 'Новость сайта'
        verbose_name_plural = 'Новости сайта'

    def __str__(self):
        return self.name


class Partner(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    image = models.ImageField(upload_to='img/partners', blank=True, null=True, verbose_name='Изображение')
    link = models.URLField(verbose_name='Ссылка на сайт', blank=True)
    published = models.BooleanField(default=True, verbose_name='Опубликованно')
    block = models.CharField(max_length=1, blank=True, verbose_name='Номер блока')

    class Meta:
        verbose_name = 'Партнер'
        verbose_name_plural = 'Партнеры'

    def __str__(self):
        return self.name


class Event(models.Model):

    IKC = 'Информационно-культурный центр (Пролетарская 8)'
    TSGBTYUTCHEV = 'Центральная городская библиотека имени Ф.И. Тютчева. Библио-холл(пл. Славы 1)'
    CDSCH = 'Центр детского и семейного чтения (Пролетарская 8)'
    BER = 'Бибилиотека эстетического развития (Керамик)'
    B2 = 'Библиотека №2 (Саввино)'
    DB = 'Детская библиотека (Павлино)'
    B4 = 'Библиотека №4 (Павлино)'
    B3 = 'Библиотека №3 (Кучино)'

    BIB_CHOICES = (
        (IKC, 'Информационно-культурный центр (Пролетарская 8)'),
        (TSGBTYUTCHEV, 'Центральная городская библиотека имени Ф.И. Тютчева. Библио-холл(пл. Славы 1)'),
        (CDSCH, 'Центр детского и семейного чтения (Пролетарская 8)'),
        (BER, 'Бибилиотека эстетического развития (Керамик)'),
        (B2, 'Библиотека №2 (Саввино)'),
        (DB, 'Детская библиотека (Павлино)'),
        (B4, 'Библиотека №4 (Павлино)'),
        (B3, 'Библиотека №3 (Кучино)'),
    )

    name = models.CharField(max_length=100, verbose_name='Название события')
    library = models.CharField(max_length=150, choices=BIB_CHOICES, default=IKC,
                               verbose_name='Выбор Библиотеки')
    date = models.DateField(default=date.today, verbose_name='Дата проведения')
    description = models.TextField(blank=True, verbose_name='Описание')
    image = models.ImageField(upload_to='img/events', blank=True, null=True, verbose_name='Изображение')

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'

    @property
    def is_past_due(self):
        return date.today() > self.date

    def __str__(self):
        return f"{self.name} | {self.date}"


class Cinema(models.Model):
    name = models.CharField(max_length=100, verbose_name='тема кинозала')
    date = models.DateField(default=date.today, verbose_name='Дата проведения')
    image = models.ImageField(upload_to='img/events', blank=True, null=True, verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'Кинозал'
        verbose_name_plural = 'Темы кинозала'

    def __str__(self):
        return f"{self.name} | {self.date}"


class Shedule(models.Model):
    name = models.CharField(max_length=100, verbose_name='Системное расписание')
    date = models.DateField(default=date.today, verbose_name='Дата версии')
    image = models.ImageField(upload_to='img/events', blank=True, null=True, verbose_name='Изображение')

    class Meta:
        verbose_name = 'Системное расписание'
        verbose_name_plural = 'Системные расписания'

    def __str__(self):
        return f"{self.name} | {self.date}"


# FORMS
class Book(models.Model, EmailSignalMixin):
    IKC = 'Информационно-культурный центр (Пролетарская 8)'
    CDSCH = 'Центр детского и семейного чтения (Пролетарская 8)'
    BER = 'Бибилиотека эстетического развития (Керамик)'
    B2 = 'Библиотека №2 (Саввино)'
    B4 = 'Библиотека №4 (Павлино)'
    B3 = 'Библиотека №3 (Кучино)'
    CHILD = 'Дошкольники'
    YOUNG = 'Начальные классы'
    OLD = 'Старшие классы'
    G1 = 'Гимназия №1'
    G2 = 'Гимназия №2'
    G11 = 'Гимназия №11'
    SC5 = 'Школа №5'
    SC7 = 'Школа №7'
    SC10 = 'Школа №10'
    SC14 = 'Школа №14'
    SC15 = 'Школа №15'
    PR = 'Прочие'

    BIB_CHOICES = (
        (IKC, 'Информационно-культурный центр (Пролетарская 8)'),
        (CDSCH, 'Центр детского и семейного чтения (Пролетарская 8)'),
        (BER, 'Бибилиотека эстетического развития (Керамик)'),
        (B2, 'Библиотека №2 (Саввино)'),
        (B4, 'Библиотека №4 (Павлино)'),
        (B3, 'Библиотека №3 (Кучино)'),
    )
    AGE_CHOICES = (
        (CHILD, 'Дошкольники'),
        (YOUNG, 'Начальные классы'),
        (OLD, 'Старшие классы')
    )
    SCHOOL_CHOICES = (
        (G1, 'Гимназия №1'),
        (G2, 'Гимназия №2'),
        (G11, 'Гимназия №11'),
        (SC5, 'Школа №5'),
        (SC7, 'Школа №7'),
        (SC10, 'Школа №10'),
        (SC14, 'Школа №14'),
        (SC15, 'Школа №15'),
        (PR, 'Прочие')
    )


    library = models.CharField(max_length=150, choices=BIB_CHOICES, verbose_name='Выбор Библиотеки')
    age = models.CharField(max_length=50, choices=AGE_CHOICES, blank=True, null=True, verbose_name='Выбор возраста')
    school = models.CharField(max_length=50, choices=SCHOOL_CHOICES, blank=True, null=True, verbose_name='Выбор школы/гимназии')
    datetime = models.DateTimeField(auto_now=True, verbose_name='Дата')
    fio = models.CharField(max_length=200, verbose_name='ФИО')
    bilet = models.CharField(max_length=18, verbose_name='№ читательского билета', blank=True)
    phone = models.CharField(max_length=17, blank=True, verbose_name='Номер елефона')
    email = models.EmailField(verbose_name='Е-мэйл')
    comment = models.TextField(max_length=300, verbose_name='Комментарий')

    class Meta:
        verbose_name = 'Форма продления книг'
        verbose_name_plural = 'Формы продления книг'

    def __str__(self):
        return f"{self.fio} | {self.datetime}"


class Question(models.Model):
    category = models.ForeignKey(Category, default='Вопрос библиотекарю', blank=True, related_name='questions',
                                 on_delete=models.SET_NULL, null=True, verbose_name='Категория')
    name = models.CharField(max_length=35, verbose_name='Имя')
    email = models.EmailField(verbose_name='Е-мэйл')
    phone = models.CharField(max_length=17, blank=True, verbose_name='Номер телефона')
    comment = models.TextField(verbose_name='Вопрос')

    class Meta:
        verbose_name = 'Вопрос библиотекарю'
        verbose_name_plural = 'Вопросы библиотекарю'

    def __str__(self):
        return self.name


class Feedback(models.Model, EmailSignalMixin):
    name = models.CharField(max_length=35, verbose_name='Имя')
    email = models.EmailField(verbose_name='Е-мэйл')
    phone = models.CharField(max_length=17, blank=True, verbose_name='Номер телефона')
    comment = models.TextField(max_length=350, verbose_name='Комментарий')

    class Meta:
        verbose_name = 'Форма обратной связи'
        verbose_name_plural = 'Формы обратной связи'

    def __str__(self):
        return self.name


class Bookrequest(models.Model, EmailSignalMixin):
    name = models.CharField(max_length=35, verbose_name='Имя')
    email = models.EmailField(verbose_name='Е-мэйл')
    comment = models.TextField(max_length=350, verbose_name='Список книг')

    class Meta:
        verbose_name = 'Комплектование'
        verbose_name_plural = 'Комплектование'

    def __str__(self):
        return self.name


class Service(models.Model):
    category = models.ForeignKey(Category, blank=True, on_delete=models.SET_NULL, related_name='services',
                                 null=True, verbose_name='Категория')
    name = models.CharField(max_length=200, verbose_name='Название услуги')
    time = models.CharField(max_length=3, blank=True, verbose_name='Время')
    ed_izm = models.CharField(max_length=100, blank=True, verbose_name='Название')
    price = models.CharField(max_length=100, blank=True, verbose_name='Цена')

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return self.name


class Service_dop(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название услуги')
    ed_izm = models.CharField(max_length=100, blank=True, verbose_name='Время/кол-во')
    price = models.CharField(max_length=100, blank=True, verbose_name='Цена')

    class Meta:
        verbose_name = 'Дополнительная услуга'
        verbose_name_plural = 'Дополнительные услуги'

    def __str__(self):
        return self.name


class ServiceDop(models.Model):
    date = models.DateField(verbose_name='Дата', default=date.today)
    fio = models.CharField(max_length=200, verbose_name='ФИО')
    phone = models.CharField(max_length=17, blank=True, verbose_name='Номер телефона')
    email = models.EmailField(verbose_name='Е-мэйл')
    comment = models.TextField(verbose_name='Комментарий')
    file = models.FileField(upload_to='img/files', verbose_name='Файл', blank=True, null=True)

    class Meta:
        verbose_name = 'Форма дополнительной услуги'
        verbose_name_plural = 'Формы дополнительных услуг'

    def __str__(self):
        return f"{self.date} | {self.fio} | {self.phone} | {self.comment}"


class Document(models.Model):
    date = models.DateField(default=date.today, verbose_name='Дата')
    name = models.CharField(max_length=250, verbose_name='Заголовок')
    slug = models.SlugField(null=True, unique=True, verbose_name='Псевдоним')
    category = models.ForeignKey(Category, blank=True, on_delete=models.SET_NULL, related_name='documents', null=True, verbose_name='Категория')
    description = models.TextField(verbose_name='Текст')
    image = models.ImageField(upload_to='img/news', blank=True, null=True, verbose_name='Главное фото')
    published = models.BooleanField(default=True, verbose_name='Опубликована')

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'

    def __str__(self):
        return self.name


class Raiting(models.Model):
    date = models.DateField(default=date.today, verbose_name='Дата')
    name = models.CharField(max_length=250, verbose_name='Заголовок')
    slug = models.SlugField(null=True, unique=True, verbose_name='Псевдоним')
    category = models.ForeignKey(Category, blank=True, on_delete=models.SET_NULL, related_name='raitings', null=True, verbose_name='Категория')
    description = models.TextField(verbose_name='Текст')
    image = models.ImageField(upload_to='img/news', blank=True, null=True, verbose_name='Главное фото')
    published = models.BooleanField(default=True, verbose_name='Опубликована')

    class Meta:
        verbose_name = 'Оценка качества'
        verbose_name_plural = 'Оценки качества'

    def __str__(self):
        return self.name


class Vacancy(models.Model):
    date = models.DateField(default=date.today, verbose_name='Дата')
    name = models.CharField(max_length=250, verbose_name='Заголовок')
    slug = models.SlugField(null=True, unique=True, verbose_name='Псевдоним')
    category = models.ForeignKey(Category, blank=True, on_delete=models.SET_NULL, related_name='vacancies', null=True, verbose_name='Категория')
    salary = models.CharField(max_length=5, verbose_name='Оклад')
    description = models.TextField(verbose_name='Текст')
    image = models.ImageField(upload_to='img/vacancy', blank=True, null=True, verbose_name='Главное фото')
    published = models.BooleanField(default=True, verbose_name='Опубликована')

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'

    def __str__(self):
        return self.name


class TermsOfUse(models.Model):
    date = models.DateField(default=date.today, verbose_name='Дата')
    name = models.CharField(max_length=100, verbose_name='Название')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    slug = models.SlugField(null=True, unique=True, verbose_name='Псевдоним')
    description = models.TextField(verbose_name='Текст')
    published = models.BooleanField(default=True, verbose_name='Опубликована')

    class Meta:
        verbose_name = 'Правила пользования'
        verbose_name_plural = 'Правила пользования'

    def __str__(self):
        return self.name


class FreeService(models.Model):
    date = models.DateField(default=date.today, verbose_name='Дата')
    name = models.CharField(max_length=100, verbose_name='Название')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    slug = models.SlugField(null=True, unique=True, verbose_name='Псевдоним')
    description = models.TextField(verbose_name='Текст')
    published = models.BooleanField(default=True, verbose_name='Опубликована')

    class Meta:
        verbose_name = 'Бесплатные услуги'
        verbose_name_plural = 'Бесплатные услуги'

    def __str__(self):
        return self.name


class VeteranVOV(models.Model):
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    middle_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='Отчество')
    image = models.ImageField(upload_to='img/veterans/vov', null=True, blank=True, verbose_name='Фото')
    description = models.TextField(verbose_name='Текст')

    class Meta:
        verbose_name = 'Данные ветерана'
        verbose_name_plural = 'Ветераны ВОВ'

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class VeteranTruda(models.Model):
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    middle_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='Отчество')
    image = models.ImageField(upload_to='img/veterans/tyl', null=True, blank=True, verbose_name='Фото')
    description = models.TextField(verbose_name='Текст')

    class Meta:
        verbose_name = 'Труженик тыла'
        verbose_name_plural = 'Труженики тыла'

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class LeningradResident(models.Model):
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    middle_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='Отчество')
    image = models.ImageField(upload_to='img/veterans/lg', null=True, blank=True, verbose_name='Фото')
    description = models.TextField(verbose_name='Текст')

    class Meta:
        verbose_name = 'Данные жителя Блокадного Лениграда'
        verbose_name_plural = 'Жители Блокадного Ленинграда'

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class HeroMemoryBook(models.Model):
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    middle_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='Отчество')
    image = models.ImageField(upload_to='img/veterans/tyl', null=True, blank=True, verbose_name='Фото')
    description = models.TextField(verbose_name='Текст')

    class Meta:
        verbose_name = 'Герой книги памяти'
        verbose_name_plural = 'Герои книги памяти'

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Anons(models.Model):
    title = models.CharField(max_length=100, verbose_name='Наименование анонса')
    description = models.TextField(verbose_name='Текст')
    active = models.BooleanField(default=False, verbose_name='Виден на главной?')

    class Meta:
        verbose_name = 'Анонс'
        verbose_name_plural = 'Анонсы библиотеки'

    def __str__(self):
        return self.title


class Library(models.Model):
    title = models.CharField(max_length=200, verbose_name='Наименование')
    author = models.ForeignKey('Author', blank=True, on_delete=models.SET_NULL, null=True, verbose_name='Автор')
    category = models.ForeignKey('LibraryCategory', blank=True, on_delete=models.SET_NULL, null=True, verbose_name = 'Категория')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='img/books/images', blank=True, verbose_name='Изображение')
    link = models.URLField(verbose_name='Ссылка на PDF файл', blank=True)
    file = models.FileField(upload_to='img/books/files', blank=True, verbose_name='Файл')
    views = models.IntegerField(default=0, verbose_name='Количество просмотров')

    class Meta:
        verbose_name = 'Электронная книга'
        verbose_name_plural = 'Электонные книги'

    def __str__(self):
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя автора')

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def __str__(self):
        return self.name


class LibraryCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование категории')

    class Meta:
        verbose_name = 'Категория электронной библиотеки'
        verbose_name_plural = 'Категории электронной библиотеки'

    def __str__(self):
        return self.name


class CinemaWeek(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    start_date = models.DateField(verbose_name='Первое число недели', blank=True, null=True)
    end_date = models.DateField(verbose_name='Последнее число недели', blank=True, null=True)
    active = models.BooleanField(default=False, verbose_name='Текущая рабочая неделя')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for cinemaday in self.cinemadays.filter(cinemaweek=self):
            for movie in cinemaday.movies.all():
                movie.save()

    class Meta:
        verbose_name = 'Неделя киносеансов ИКЦ'
        verbose_name_plural = 'Недели киносеансов ИКЦ'

    def __str__(self):
        return self.name


class CinemaDay(models.Model):
    name = models.CharField(max_length=15, verbose_name='День киносеанса')
    date = models.DateField(verbose_name='Дата')
    cinemaweek = models.ForeignKey(CinemaWeek, on_delete=models.CASCADE, verbose_name='Неделя киноафишы', related_name='cinemadays')

    class Meta:
        verbose_name = 'День сеансов ИКЦ'
        verbose_name_plural = 'Дни сеансов ИКЦ'

    def __str__(self):
        return self.name


class Movie(models.Model):
    cinemaday = models.ForeignKey(CinemaDay, on_delete=models.CASCADE, null=True, verbose_name='День недели', related_name='movies')
    name = models.CharField(max_length=150, blank=True, verbose_name='Название')
    start_time = models.TimeField(blank=True, null=True, verbose_name='Время начала')

    class Meta:
        verbose_name = 'Фильм ИКЦ'
        verbose_name_plural = 'Фильмы ИКЦ'

    def __str__(self):
        return self.name

"""Schedules"""


class Week(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    start_date = models.DateField(verbose_name='Первое число недели', blank=True, null=True)
    end_date = models.DateField(verbose_name='Последнее число недели', blank=True, null=True)
    active = models.BooleanField(default=False, verbose_name='Текущая рабочая неделя')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for day in self.days.filter(week=self):  # здесь было изменено
            for event in day.events.all():  # и здесь тоже
                event.save()

    class Meta:
        verbose_name = 'Расписание ИКЦ'
        verbose_name_plural = 'Расписания ИКЦ'

    def __str__(self):
        return self.name


class Day(models.Model):
    name = models.CharField(max_length=15, verbose_name='День недели')
    date = models.DateField(verbose_name='Дата', blank=True, null=True)
    week = models.ForeignKey(Week, on_delete=models.CASCADE, verbose_name='Неделя', related_name='days')

    class Meta:
        verbose_name = 'Рабочий день ИКЦ'
        verbose_name_plural = 'Рабочий день ИКЦ'

    def __str__(self):
        return self.name


class Eventy(models.Model):

    ZERO = '0+'
    SIX = '6+'
    TWELVE = '12+'
    FOURTEEN = '14+'
    SIXTEEN = '16+'
    EIGHTEEN = '18+'
    FIFTYFIVE = '55+'
    SIXTY = '60+'
    SIXTYFIVE = '65+'

    AGE_CHOICES = (
        (ZERO, '0+'),
        (SIX, '6+'),
        (TWELVE, '12+'),
        (FOURTEEN, '14+'),
        (SIXTEEN, '16+'),
        (EIGHTEEN, '18+'),
        (FIFTYFIVE, '55+'),
        (SIXTY, '60+'),
        (SIXTYFIVE, '65+'),

    )

    day = models.ForeignKey(Day, on_delete=models.CASCADE, null=True, verbose_name='День недели', related_name='events')
    name = models.CharField(max_length=150, blank=True, verbose_name='Название')
    payment = models.BooleanField(default=False, verbose_name='Платное')
    booking =  models.BooleanField(default=False, verbose_name='Запись')
    age = models.CharField(max_length=50, choices=AGE_CHOICES, blank=True, null=True, verbose_name='Возраст')
    start_time = models.TimeField(blank=True, null=True, verbose_name='Время начала')
    end_time = models.TimeField(blank=True, null=True, verbose_name='Время окончания')

    class Meta:
        verbose_name = 'Мероприятие ИКЦ'
        verbose_name_plural = 'Мероприятия ИКЦ'

    def __str__(self):
        return self.name

class WeekCDSCH(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    start_date = models.DateField(verbose_name='Первое число недели', blank=True, null=True)
    end_date = models.DateField(verbose_name='Последнее число недели', blank=True, null=True)
    active = models.BooleanField(default=False, verbose_name='Текущая рабочая неделя')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for day in self.days.filter(week=self):
            for event in day.events.all():
                event.save()

    class Meta:
        verbose_name = 'Расписание ЦДСЧ'
        verbose_name_plural = 'Расписания ЦДСЧ'

    def __str__(self):
        return self.name


class DayCDSCH(models.Model):
    name = models.CharField(max_length=15, verbose_name='День недели')
    date = models.DateField(verbose_name='Дата', blank=True, null=True)
    week = models.ForeignKey(WeekCDSCH, on_delete=models.CASCADE, verbose_name='Неделя', related_name='days')

    class Meta:
        verbose_name = 'Рабочий день ЦДСЧ'
        verbose_name_plural = 'Рабочий день ЦДСЧ'

    def __str__(self):
        return self.name


class EventyCDSCH(models.Model):
    ZERO = '0+'
    SIX = '6+'
    TWELVE = '12+'
    FOURTEEN = '14+'
    SIXTEEN = '16+'
    EIGHTEEN = '18+'
    FIFTYFIVE = '55+'
    SIXTY = '60+'
    SIXTYFIVE = '65+'

    AGE_CHOICES = (
        (ZERO, '0+'),
        (SIX, '6+'),
        (TWELVE, '12+'),
        (FOURTEEN, '14+'),
        (SIXTEEN, '16+'),
        (EIGHTEEN, '18+'),
        (FIFTYFIVE, '55+'),
        (SIXTY, '60+'),
        (SIXTYFIVE, '65+'),

    )

    day = models.ForeignKey(DayCDSCH, on_delete=models.CASCADE, null=True, verbose_name='День недели',
                            related_name='events')
    name = models.CharField(max_length=150, blank=True, verbose_name='Название')
    payment = models.BooleanField(default=False, verbose_name='Платное')
    booking =  models.BooleanField(default=False, verbose_name='Запись')
    age = models.CharField(max_length=50, choices=AGE_CHOICES, blank=True, null=True, verbose_name='Возраст')
    start_time = models.TimeField(blank=True, null=True, verbose_name='Время начала')
    end_time = models.TimeField(blank=True, null=True, verbose_name='Время окончания')

    class Meta:
        verbose_name = 'Мероприятие ЦДСЧ'
        verbose_name_plural = 'Мероприятия ЦДСЧ'

    def __str__(self):
        return self.name


class WeekBER(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    start_date = models.DateField(verbose_name='Первое число недели', blank=True, null=True)
    end_date = models.DateField(verbose_name='Последнее число недели', blank=True, null=True)
    active = models.BooleanField(default=False, verbose_name='Текущая рабочая неделя')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for day in self.days.filter(week=self):
            for event in day.events.all():
                event.save()

    class Meta:
        verbose_name = 'Расписание БЭР'
        verbose_name_plural = 'Расписания БЭР'

    def __str__(self):
        return self.name

class DayBER(models.Model):
    name = models.CharField(max_length=15, verbose_name='День недели')
    date = models.DateField(verbose_name='Дата', blank=True, null=True)
    week = models.ForeignKey(WeekBER, on_delete=models.CASCADE, verbose_name='Неделя', related_name='days')

    class Meta:
        verbose_name = 'Рабочий день БЭР'
        verbose_name_plural = 'Рабочий день БЭР'

    def __str__(self):
        return self.name


class EventyBER(models.Model):
    ZERO = '0+'
    SIX = '6+'
    TWELVE = '12+'
    FOURTEEN = '14+'
    SIXTEEN = '16+'
    EIGHTEEN = '18+'
    FIFTYFIVE = '55+'
    SIXTY = '60+'
    SIXTYFIVE = '65+'

    AGE_CHOICES = (
        (ZERO, '0+'),
        (SIX, '6+'),
        (TWELVE, '12+'),
        (FOURTEEN, '14+'),
        (SIXTEEN, '16+'),
        (EIGHTEEN, '18+'),
        (FIFTYFIVE, '55+'),
        (SIXTY, '60+'),
        (SIXTYFIVE, '65+'),

    )

    day = models.ForeignKey(DayBER, on_delete=models.CASCADE, null=True, verbose_name='День недели', related_name='events')
    name = models.CharField(max_length=150, blank=True, verbose_name='Название')
    payment = models.BooleanField(default=False, verbose_name='Платное')
    booking =  models.BooleanField(default=False, verbose_name='Запись')
    age = models.CharField(max_length=50, choices=AGE_CHOICES, blank=True, null=True, verbose_name='Возраст')
    start_time = models.TimeField(blank=True, null=True, verbose_name='Время начала')
    end_time = models.TimeField(blank=True, null=True, verbose_name='Время окончания')

    class Meta:
        verbose_name = 'Мероприятие БЭР'
        verbose_name_plural = 'Мероприятия БЭР'

    def __str__(self):
        return self.name


class WeekF2(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    start_date = models.DateField(verbose_name='Первое число недели', blank=True, null=True)
    end_date = models.DateField(verbose_name='Последнее число недели', blank=True, null=True)
    active = models.BooleanField(default=False, verbose_name='Текущая рабочая неделя')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for day in self.days.filter(week=self):
            for event in day.events.all():
                event.save()

    class Meta:
        verbose_name = 'Расписание Ф2'
        verbose_name_plural = 'Расписания Ф2'

    def __str__(self):
        return self.name



class DayF2(models.Model):
    name = models.CharField(max_length=15, verbose_name='День недели')
    date = models.DateField(verbose_name='Дата', blank=True, null=True)
    week = models.ForeignKey(WeekF2, on_delete=models.CASCADE, verbose_name='Неделя', related_name='days')

    class Meta:
        verbose_name = 'Рабочий день Ф2'
        verbose_name_plural = 'Рабочие дни Ф2'

    def __str__(self):
        return self.name


class EventyF2(models.Model):
    ZERO = '0+'
    SIX = '6+'
    TWELVE = '12+'
    FOURTEEN = '14+'
    SIXTEEN = '16+'
    EIGHTEEN = '18+'
    FIFTYFIVE = '55+'
    SIXTY = '60+'
    SIXTYFIVE = '65+'

    AGE_CHOICES = (
        (ZERO, '0+'),
        (SIX, '6+'),
        (TWELVE, '12+'),
        (FOURTEEN, '14+'),
        (SIXTEEN, '16+'),
        (EIGHTEEN, '18+'),
        (FIFTYFIVE, '55+'),
        (SIXTY, '60+'),
        (SIXTYFIVE, '65+'),

    )

    day = models.ForeignKey(DayF2, on_delete=models.CASCADE, null=True, verbose_name='День недели', related_name='events')
    name = models.CharField(max_length=150, blank=True, verbose_name='Название')
    payment = models.BooleanField(default=False, verbose_name='Платное')
    booking =  models.BooleanField(default=False, verbose_name='Запись')
    age = models.CharField(max_length=50, choices=AGE_CHOICES, blank=True, null=True, verbose_name='Возраст')
    start_time = models.TimeField(blank=True, null=True, verbose_name='Время начала')
    end_time = models.TimeField(blank=True, null=True, verbose_name='Время окончания')

    class Meta:
        verbose_name = 'Мероприятие Ф2'
        verbose_name_plural = 'Мероприятия Ф2'

    def __str__(self):
        return self.name


class WeekF3(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    start_date = models.DateField(verbose_name='Первое число недели', blank=True, null=True)
    end_date = models.DateField(verbose_name='Последнее число недели', blank=True, null=True)
    active = models.BooleanField(default=False, verbose_name='Текущая рабочая неделя')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for day in self.days.filter(week=self):
            for event in day.events.all():
                event.save()

    class Meta:
        verbose_name = 'Расписание Ф3'
        verbose_name_plural = 'Расписания Ф3'

    def __str__(self):
        return self.name


class DayF3(models.Model):
    name = models.CharField(max_length=15, verbose_name='День недели')
    date = models.DateField(verbose_name='Дата', blank=True, null=True)
    week = models.ForeignKey(WeekF3, on_delete=models.CASCADE, verbose_name='Неделя', related_name='days')

    class Meta:
        verbose_name = 'Рабочий день Ф3'
        verbose_name_plural = 'Рабочий день Ф3'

    def __str__(self):
        return self.name


class EventyF3(models.Model):
    ZERO = '0+'
    SIX = '6+'
    TWELVE = '12+'
    FOURTEEN = '14+'
    SIXTEEN = '16+'
    EIGHTEEN = '18+'
    FIFTYFIVE = '55+'
    SIXTY = '60+'
    SIXTYFIVE = '65+'

    AGE_CHOICES = (
        (ZERO, '0+'),
        (SIX, '6+'),
        (TWELVE, '12+'),
        (FOURTEEN, '14+'),
        (SIXTEEN, '16+'),
        (EIGHTEEN, '18+'),
        (FIFTYFIVE, '55+'),
        (SIXTY, '60+'),
        (SIXTYFIVE, '65+'),

    )

    day = models.ForeignKey(DayF3, on_delete=models.CASCADE, null=True, verbose_name='День недели', related_name='events')
    name = models.CharField(max_length=150, blank=True, verbose_name='Название')
    payment = models.BooleanField(default=False, verbose_name='Платное')
    booking =  models.BooleanField(default=False, verbose_name='Запись')
    age = models.CharField(max_length=50, choices=AGE_CHOICES, blank=True, null=True, verbose_name='Возраст')
    start_time = models.TimeField(blank=True, null=True, verbose_name='Время начала')
    end_time = models.TimeField(blank=True, null=True, verbose_name='Время окончания')

    class Meta:
        verbose_name = 'Мероприятие Ф3'
        verbose_name_plural = 'Мероприятия Ф3'

    def __str__(self):
        return self.name


class WeekF4(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    start_date = models.DateField(verbose_name='Первое число недели', blank=True, null=True)
    end_date = models.DateField(verbose_name='Последнее число недели', blank=True, null=True)
    active = models.BooleanField(default=False, verbose_name='Текущая рабочая неделя')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for day in self.days.filter(week=self):
            for event in day.events.all():
                event.save()

    class Meta:
        verbose_name = 'Расписание Ф4'
        verbose_name_plural = 'Расписания Ф4'

    def __str__(self):
        return self.name


class DayF4(models.Model):
    name = models.CharField(max_length=15, verbose_name='День недели')
    date = models.DateField(verbose_name='Дата', blank=True, null=True)
    week = models.ForeignKey(WeekF4, on_delete=models.CASCADE, verbose_name='Неделя', related_name='days')

    class Meta:
        verbose_name = 'Рабочий день Ф4'
        verbose_name_plural = 'Рабочий день Ф4'

    def __str__(self):
        return self.name


class EventyF4(models.Model):
    ZERO = '0+'
    SIX = '6+'
    TWELVE = '12+'
    FOURTEEN = '14+'
    SIXTEEN = '16+'
    EIGHTEEN = '18+'
    FIFTYFIVE = '55+'
    SIXTY = '60+'
    SIXTYFIVE = '65+'

    AGE_CHOICES = (
        (ZERO, '0+'),
        (SIX, '6+'),
        (TWELVE, '12+'),
        (FOURTEEN, '14+'),
        (SIXTEEN, '16+'),
        (EIGHTEEN, '18+'),
        (FIFTYFIVE, '55+'),
        (SIXTY, '60+'),
        (SIXTYFIVE, '65+'),

    )

    day = models.ForeignKey(DayF4, on_delete=models.CASCADE, null=True, verbose_name='День недели', related_name='events')
    name = models.CharField(max_length=150, blank=True, verbose_name='Название')
    payment = models.BooleanField(default=False, verbose_name='Платное')
    booking =  models.BooleanField(default=False, verbose_name='Запись')
    age = models.CharField(max_length=50, choices=AGE_CHOICES, blank=True, null=True, verbose_name='Возраст')
    start_time = models.TimeField(blank=True, null=True, verbose_name='Время начала')
    end_time = models.TimeField(blank=True, null=True, verbose_name='Время окончания')

    class Meta:
        verbose_name = 'Мероприятие Ф4'
        verbose_name_plural = 'Мероприятия Ф4'

    def __str__(self):
        return self.name
















