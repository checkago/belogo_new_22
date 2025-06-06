from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from datetime import datetime, date

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
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

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
    qrcode = models.ImageField(upload_to='img/cbs', blank=True, null=True, verbose_name='QR-код')
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
    library = models.ForeignKey(Biblioteka, blank=True, on_delete=models.SET_NULL, null=True, verbose_name='Библиотека')
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


class Project(models.Model):
    theme = models.ForeignKey('ProjectTheme', on_delete=models.CASCADE, verbose_name='Общая тема проекта')
    library = models.ForeignKey(Biblioteka, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Выбор Библиотеки')
    title = models.CharField(max_length=150, blank=True, verbose_name='Название')
    date = models.DateField(default=date.today, blank=True, verbose_name='Дата')
    file = models.FileField(upload_to='media/projects', verbose_name='Файл', blank=True)
    link = models.URLField(blank=True, verbose_name='Ссылка на PDF')

    class Meta:
        verbose_name = 'Проект года'
        verbose_name_plural = 'Проекты года'

    def __str__(self):
        return self.library.name


class ProjectTheme(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название темы проектов')

    class Meta:
        verbose_name = 'Тема проектов'
        verbose_name_plural = 'Темы проектов'

    def __str__(self):
        return self.name


class Project_other(models.Model):
    title = models.CharField(max_length=150, blank=True, verbose_name='Название')
    date = models.DateField(default=date.today, blank=True, verbose_name='Дата')
    image = models.ImageField(upload_to='media/projects_other/img', blank=True, verbose_name='Изображение')
    file_pdf = models.FileField(upload_to='media/projects_other', verbose_name='Файл pdf', blank=True)
    file = models.FileField(upload_to='media/projects_other', verbose_name='Файл (разное)', blank=True)
    link = models.URLField(blank=True, verbose_name='Ссылка на PDF')

    class Meta:
        verbose_name = 'Наш проект'
        verbose_name_plural = 'Наши проекты'

    def __str__(self):
        return self.title


class AuthorArticle(models.Model):
    name = models.CharField(max_length=240, verbose_name='ФИО автора')

    class Meta:
        verbose_name = 'Наш Автор'
        verbose_name_plural = 'Наши авторы'

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=150, blank=True, verbose_name='Название')
    date = models.DateField(default=date.today, blank=True, verbose_name='Дата')
    author = models.ForeignKey(AuthorArticle, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Автор')
    project = models.ForeignKey(Project_other, on_delete=models.CASCADE, null=True, blank=True, verbose_name='К проекту')
    image = models.ImageField(upload_to='media/projects_other/img', blank=True, verbose_name='Изображение')
    description = models.TextField(blank=True, verbose_name='Преамбула')
    file_pdf = models.FileField(upload_to='media/projects_other', verbose_name='Файл pdf', blank=True)
    file = models.FileField(upload_to='media/projects_other', blank=True, verbose_name='Файл (разное)')
    link = models.URLField(blank=True, verbose_name='Ссылка на PDF')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title

class Event(models.Model):

    IKC = 'Информационно-культурный центр'
    TSGBTYUTCHEV = 'Центральная городская библиотека имени Ф.И. Тютчева'
    CDSCH = 'Центр детского и семейного чтения'
    BER = 'Бибилиотека эстетического развития'
    B2 = 'Библиотека №2'
    B3 = 'Библиотека №3'
    B4 = 'Библиотека №4'
    B5 = 'Библиотека №5'
    DB = 'Детская библиотека'
    BCY = 'Библиотечный центр "Южный"'
    BSCHD = 'Библиотека семейного чтения им. Н.Ф.Дмитриева'
    YUB = 'Юношеская библиотека'
    NB = 'Никольская библиотека'
    NAB = 'Никольско-Архангельская библиотека'
    PPB = 'Пехра-Покровская библиотека'
    FB = 'Федурновская сельская библиотека'
    NMB = 'Новомилетская сельская библиотека'
    SB = 'Соболихинская сельская библиотека'
    CHB = 'Черновская сельская библиотека'


    BIB_CHOICES = (
        (IKC, 'Информационно-культурный центр'),
        (TSGBTYUTCHEV, 'Центральная городская библиотека имени Ф.И. Тютчева'),
        (CDSCH, 'Центр детского и семейного чтения'),
        (BER, 'Бибилиотека эстетического развития'),
        (B2, 'Библиотека №2'),
        (B3, 'Библиотека №3'),
        (B4, 'Библиотека №4'),
        (B5, 'Библиотека №5'),
        (DB, 'Детская библиотека'),
        (BCY, 'Библиотечный центр "Южный"'),
        (BSCHD, 'Библиотека семейного чтения им. Н.Ф.Дмитриева'),
        (YUB, 'Юношеская библиотека'),
        (NB, 'Никольская библиотека'),
        (NAB, 'Никольско-Архангельская библиотека'),
        (PPB, 'Пехра-Покровская библиотека'),
        (FB, 'Федурновская сельская библиотека'),
        (NMB, 'Новомилетская сельская библиотека'),
        (SB, 'Соболихинская сельская библиотека'),
        (CHB, 'Черновская сельская библиотека')
    )

    name = models.CharField(max_length=100, verbose_name='Название события')
    library = models.CharField(max_length=150, choices=BIB_CHOICES, default=IKC,
                               verbose_name='Выбор Библиотеки')
    date = models.DateTimeField(verbose_name='Дата и время начала')
    date_end = models.DateTimeField(null=True, blank=True, verbose_name='Дата и время окончания')
    description = models.TextField(blank=True, verbose_name='Описание')
    image = models.ImageField(upload_to='img/events', blank=True, null=True, verbose_name='Изображение')

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'

    @property
    def is_past_due(self):
        today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        return today > self.date

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
    TSGBTYUTCHEV = 'Центральная городская библиотека имени Ф.И. Тютчева.(пл. Славы 1)'
    CDSCH = 'Центр детского и семейного чтения (Пролетарская 8)'
    BER = 'Бибилиотека эстетического развития (Керамик)'
    B2 = 'Библиотека №2 (Саввино)'
    B3 = 'Библиотека №3 (Кучино)'
    B4 = 'Библиотека №4 (Павлино)'
    B5 = 'Библиотека №5 (Заря)'
    DB = 'Детская библиотека (ш. Энтузиастов 33)'
    BCY = 'Библиотечный центр "Южный" (Твардовского 5)'
    BSCHD = 'Библиотека семейного чтения им. Н.Ф.Дмитриева'
    YUB = 'Юношеская библиотека (Спортивная 17)'
    NB = 'Никольская библиотека'
    NAB = 'Никольско-Архангельская библиотека'
    PPB = 'Пехра-Покровская библиотека'
    FB = 'Федурновская библиотека'
    NMB = 'Новомилетская библиотека'
    SB = 'Соболихинская библиотека'
    CHB = 'Черновская библиотека'
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
        (TSGBTYUTCHEV, 'Центральная городская библиотека имени Ф.И. Тютчева.(пл. Славы 1)'),
        (CDSCH, 'Центр детского и семейного чтения (Пролетарская 8)'),
        (BER, 'Бибилиотека эстетического развития (Керамик)'),
        (B2, 'Библиотека №2 (Саввино)'),
        (B3, 'Библиотека №3 (Кучино)'),
        (B4, 'Библиотека №4 (Павлино)'),
        (B5, 'Библиотека №5 (Заря)'),
        (DB, 'Детская библиотека (ш. Энтузиастов 33)'),
        (BCY, 'Библиотечный центр "Южный" (Твардовского 5)'),
        (BSCHD, 'Библиотека семейного чтения им. Н.Ф.Дмитриева'),
        (YUB, 'Юношеская библиотека (Спортивная 17)'),
        (NB, 'Никольская библиотека'),
        (NAB, 'Никольско-Архангельская библиотека'),
        (PPB, 'Пехра-Покровская библиотека'),
        (FB, 'Федурновская библиотека'),
        (NMB, 'Новомилетская библиотека'),
        (SB, 'Соболихинская библиотека'),
        (CHB, 'Черновская библиотека'),
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
    phone = models.CharField(max_length=17, blank=True, verbose_name='Номер телефона')
    email = models.EmailField(verbose_name='Е-мэйл')
    comment = models.TextField(max_length=300, verbose_name='Комментарий')
    agreement = models.BooleanField(default=False, verbose_name='Согласие(персональные данные)')

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
    agreement = models.BooleanField(default=False, verbose_name='Согласие(персональные данные)')

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
    agreement = models.BooleanField(default=False, verbose_name='Согласие(персональные данные)')

    class Meta:
        verbose_name = 'Форма обратной связи'
        verbose_name_plural = 'Формы обратной связи'

    def __str__(self):
        return self.name


class Bookrequest(models.Model, EmailSignalMixin):
    name = models.CharField(max_length=35, verbose_name='Имя')
    email = models.EmailField(verbose_name='Е-мэйл')
    comment = models.TextField(max_length=350, verbose_name='Список книг')
    agreement = models.BooleanField(default=False, verbose_name='Согласие(персональные данные)')

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
    agreement = models.BooleanField(default=False, verbose_name='Согласие(персональные данные)')

    class Meta:
        verbose_name = 'Форма дополнительной услуги'
        verbose_name_plural = 'Формы дополнительных услуг'

    def __str__(self):
        return f"{self.date} | {self.fio} | {self.phone} | {self.comment}"


class Document(models.Model):
    date = models.DateField(default=date.today, verbose_name='Дата')
    name = models.CharField(max_length=250, verbose_name='Заголовок')
    category = models.ForeignKey(Category, blank=True, on_delete=models.SET_NULL, related_name='documents', null=True, verbose_name='Категория')
    description = models.TextField(verbose_name='Текст')
    image = models.ImageField(upload_to='img/news', blank=True, null=True, verbose_name='Главное фото')
    file = models.FileField(upload_to='media/projects', verbose_name='Файл', null=True, blank=True)
    published = models.BooleanField(default=True, verbose_name='Опубликована')

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'

    def __str__(self):
        return self.name


class PolojenieKonkurs(models.Model):
    date = models.DateField(default=date.today, verbose_name='Дата публикации')
    start_date = models.DateField(verbose_name='Дата начала проведения', blank=True, null=True)
    end_date = models.DateField(verbose_name='Дата окончания проведения', blank=True, null=True)
    name = models.CharField(max_length=250, verbose_name='Заголовок')
    category = models.ForeignKey(Category, default=16, blank=True, on_delete=models.SET_NULL,
                                 related_name='polojenya_konkurs', null=True, verbose_name='Категория')
    description = models.TextField(verbose_name='Текст')
    image = models.ImageField(upload_to='img/konkurs', blank=True, null=True, verbose_name='Главное фото')
    konkurs_doc = models.FileField(upload_to='documents/polojenie_k', blank=True, null=True, verbose_name='Файл положения')
    konkurs_zayavka = models.FileField(upload_to='documents/polojeni_k_z', blank=True, null=True, verbose_name='Файл Заявки')
    published = models.BooleanField(default=True, verbose_name='Опубликована')

    class Meta:
        verbose_name = 'Положение '
        verbose_name_plural = 'Положения о конкурсах'

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


class VideoMemoryBook(models.Model):
    title = models.CharField(max_length=250, verbose_name='Заголовок')
    video_file = models.FileField(upload_to='videos/')  # файл сохраняется в MEDIA_ROOT/videos/
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Видео книга памяти'
        verbose_name_plural = 'Видео для книги памяти'

    def __str__(self):
        return self.title


class Anons(models.Model):
    title = models.CharField(max_length=100, verbose_name='Наименование анонса')
    description = models.TextField(verbose_name='Текст')
    active = models.BooleanField(default=False, verbose_name='Виден на главной?')

    class Meta:
        verbose_name = 'Анонс'
        verbose_name_plural = 'Анонсы библиотеки'

    def __str__(self):
        return self.title

class BookView(models.Model):
    book = models.ForeignKey('Library', on_delete=models.CASCADE, verbose_name='Книга')
    view_count = models.PositiveIntegerField(default=1, verbose_name='Количество просмотров книги')
    viewed_at = models.DateField(default=timezone.now, verbose_name='Дата просмотра')

    class Meta:
        verbose_name = 'Просмотр'
        verbose_name_plural = 'Просмотры'

    def __str__(self):
        return f'{self.book.title} - {self.viewed_at}'


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
    """ПОЛЯ age, day, start и end доджны быть blank=True и null=True при следующих миграциях"""

    day = models.ForeignKey(Day, on_delete=models.CASCADE, verbose_name='День недели', related_name='events')
    name = models.CharField(max_length=150, verbose_name='Название')
    payment = models.BooleanField(default=False, verbose_name='Платное')
    booking = models.BooleanField(default=False, verbose_name='Запись')
    age = models.CharField(max_length=50, choices=AGE_CHOICES, default=ZERO, verbose_name='Возраст')
    start_time = models.TimeField(verbose_name='Время начала')
    end_time = models.TimeField(verbose_name='Время окончания')

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

    day = models.ForeignKey(DayCDSCH, on_delete=models.CASCADE, verbose_name='День недели',
                            related_name='events')
    name = models.CharField(max_length=150, verbose_name='Название')
    payment = models.BooleanField(default=False, verbose_name='Платное')
    booking = models.BooleanField(default=False, verbose_name='Запись')
    age = models.CharField(max_length=50, choices=AGE_CHOICES, default=ZERO, verbose_name='Возраст')
    start_time = models.TimeField(verbose_name='Время начала')
    end_time = models.TimeField(verbose_name='Время окончания')

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

    day = models.ForeignKey(DayBER, on_delete=models.CASCADE, verbose_name='День недели', related_name='events')
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

    day = models.ForeignKey(DayF2, on_delete=models.CASCADE, verbose_name='День недели', related_name='events')
    name = models.CharField(max_length=150, verbose_name='Название')
    payment = models.BooleanField(default=False, verbose_name='Платное')
    booking = models.BooleanField(default=False, verbose_name='Запись')
    age = models.CharField(max_length=50, choices=AGE_CHOICES, default=ZERO, verbose_name='Возраст')
    start_time = models.TimeField(verbose_name='Время начала')
    end_time = models.TimeField(verbose_name='Время окончания')

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

    day = models.ForeignKey(DayF3, on_delete=models.CASCADE, verbose_name='День недели', related_name='events')
    name = models.CharField(max_length=150, verbose_name='Название')
    payment = models.BooleanField(default=False, verbose_name='Платное')
    booking = models.BooleanField(default=False, verbose_name='Запись')
    age = models.CharField(max_length=50, choices=AGE_CHOICES, default=ZERO, verbose_name='Возраст')
    start_time = models.TimeField(verbose_name='Время начала')
    end_time = models.TimeField(verbose_name='Время окончания')

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

    day = models.ForeignKey(DayF4, on_delete=models.CASCADE, verbose_name='День недели', related_name='events')
    name = models.CharField(max_length=150, verbose_name='Название')
    payment = models.BooleanField(default=False, verbose_name='Платное')
    booking = models.BooleanField(default=False, verbose_name='Запись')
    age = models.CharField(max_length=50, choices=AGE_CHOICES, default=ZERO, verbose_name='Возраст')
    start_time = models.TimeField(verbose_name='Время начала')
    end_time = models.TimeField(verbose_name='Время окончания')

    class Meta:
        verbose_name = 'Мероприятие Ф4'
        verbose_name_plural = 'Мероприятия Ф4'

    def __str__(self):
        return self.name


class WeekB5(models.Model):
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
        verbose_name = 'Расписание Библиотеки №5'
        verbose_name_plural = 'Расписания Библиотеки №5'

    def __str__(self):
        return self.name


class DayB5(models.Model):
    name = models.CharField(max_length=15, verbose_name='День недели')
    date = models.DateField(verbose_name='Дата', blank=True, null=True)
    week = models.ForeignKey(WeekB5, on_delete=models.CASCADE, verbose_name='Неделя', related_name='days')

    class Meta:
        verbose_name = 'Рабочий день Библиотеки №5'
        verbose_name_plural = 'Рабочий день Библиотеки №5'

    def __str__(self):
        return self.name


class EventyB5(models.Model):
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

    day = models.ForeignKey(DayB5, on_delete=models.CASCADE, verbose_name='День недели',
                            related_name='events')
    name = models.CharField(max_length=150, verbose_name='Название')
    payment = models.BooleanField(default=False, verbose_name='Платное')
    booking = models.BooleanField(default=False, verbose_name='Запись')
    age = models.CharField(max_length=50, choices=AGE_CHOICES, default=ZERO, verbose_name='Возраст')
    start_time = models.TimeField(verbose_name='Время начала')
    end_time = models.TimeField(verbose_name='Время окончания')

    class Meta:
        verbose_name = 'Мероприятие Библиотеки №5'
        verbose_name_plural = 'Мероприятия Библиотеки №5'

    def __str__(self):
        return self.name


class WeekCGBT(models.Model):
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
        verbose_name = 'Расписание ЦГБ им. Тютчева'
        verbose_name_plural = 'Расписания ЦГБ им. Тютчева'

    def __str__(self):
        return self.name


class DayCGBT(models.Model):
    name = models.CharField(max_length=15, verbose_name='День недели')
    date = models.DateField(verbose_name='Дата', blank=True, null=True)
    week = models.ForeignKey(WeekCGBT, on_delete=models.CASCADE, verbose_name='Неделя', related_name='days')

    class Meta:
        verbose_name = 'Рабочий день ЦГБ им. Тютчева'
        verbose_name_plural = 'Рабочий день ЦГБ им. Тютчева'

    def __str__(self):
        return self.name


class EventyCGBT(models.Model):
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

    day = models.ForeignKey(DayCGBT, on_delete=models.CASCADE, verbose_name='День недели',
                            related_name='events')
    name = models.CharField(max_length=150, verbose_name='Название')
    payment = models.BooleanField(default=False, verbose_name='Платное')
    booking = models.BooleanField(default=False, verbose_name='Запись')
    age = models.CharField(max_length=50, choices=AGE_CHOICES, default=ZERO, verbose_name='Возраст')
    start_time = models.TimeField(verbose_name='Время начала')
    end_time = models.TimeField(verbose_name='Время окончания')

    class Meta:
        verbose_name = 'Мероприятие ЦГБ им. Тютчева'
        verbose_name_plural = 'Мероприятия ЦГБ им. Тютчева'

    def __str__(self):
        return self.name


class WeekBCJ(models.Model):
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
        verbose_name = 'Расписание БЦ Южный'
        verbose_name_plural = 'Расписания БЦ Южный'

    def __str__(self):
        return self.name


class DayBCJ(models.Model):
    name = models.CharField(max_length=15, verbose_name='День недели')
    date = models.DateField(verbose_name='Дата', blank=True, null=True)
    week = models.ForeignKey(WeekBCJ, on_delete=models.CASCADE, verbose_name='Неделя', related_name='days')

    class Meta:
        verbose_name = 'Рабочий день БЦ Южный'
        verbose_name_plural = 'Рабочий день БЦ Южный'

    def __str__(self):
        return self.name


class EventyBCJ(models.Model):
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

    day = models.ForeignKey(DayBCJ, on_delete=models.CASCADE, verbose_name='День недели',
                            related_name='events')
    name = models.CharField(max_length=150, verbose_name='Название')
    payment = models.BooleanField(default=False, verbose_name='Платное')
    booking = models.BooleanField(default=False, verbose_name='Запись')
    age = models.CharField(max_length=50, choices=AGE_CHOICES, default=ZERO, verbose_name='Возраст')
    start_time = models.TimeField(verbose_name='Время начала')
    end_time = models.TimeField(verbose_name='Время окончания')

    class Meta:
        verbose_name = 'Мероприятие БЦ Южный'
        verbose_name_plural = 'Мероприятия БЦ Южный'

    def __str__(self):
        return self.name


class WeekBSCD(models.Model):
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
        verbose_name = 'Расписание БСЧ им Дмитриева'
        verbose_name_plural = 'Расписания БСЧ им Дмитриева'

    def __str__(self):
        return self.name


class DayBSCD(models.Model):
    name = models.CharField(max_length=15, verbose_name='День недели')
    date = models.DateField(verbose_name='Дата', blank=True, null=True)
    week = models.ForeignKey(WeekBSCD, on_delete=models.CASCADE, verbose_name='Неделя', related_name='days')

    class Meta:
        verbose_name = 'Рабочий день БСЧ им Дмитриева'
        verbose_name_plural = 'Рабочий БСЧ им Дмитриева'

    def __str__(self):
        return self.name


class EventyBSCD(models.Model):
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

    day = models.ForeignKey(DayBSCD, on_delete=models.CASCADE, verbose_name='День недели',
                            related_name='events')
    name = models.CharField(max_length=150, verbose_name='Название')
    payment = models.BooleanField(default=False, verbose_name='Платное')
    booking = models.BooleanField(default=False, verbose_name='Запись')
    age = models.CharField(max_length=50, choices=AGE_CHOICES, default=ZERO, verbose_name='Возраст')
    start_time = models.TimeField(verbose_name='Время начала')
    end_time = models.TimeField(verbose_name='Время окончания')

    class Meta:
        verbose_name = 'Мероприятие БСЧ им Дмитриева'
        verbose_name_plural = 'Мероприятия БСЧ им Дмитриева'

    def __str__(self):
        return self.name


class WeekYB(models.Model):
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
        verbose_name = 'Расписание Юношеская библиотека'
        verbose_name_plural = 'Расписания Юношеская библиотека'

    def __str__(self):
        return self.name


class DayYB(models.Model):
    name = models.CharField(max_length=15, verbose_name='День недели')
    date = models.DateField(verbose_name='Дата', blank=True, null=True)
    week = models.ForeignKey(WeekYB, on_delete=models.CASCADE, verbose_name='Неделя', related_name='days')

    class Meta:
        verbose_name = 'Рабочий день Юношеская библиотека'
        verbose_name_plural = 'Рабочий день Юношеская библиотека'

    def __str__(self):
        return self.name


class EventyYB(models.Model):
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

    day = models.ForeignKey(DayYB, on_delete=models.CASCADE, verbose_name='День недели',
                            related_name='events')
    name = models.CharField(max_length=150, verbose_name='Название')
    payment = models.BooleanField(default=False, verbose_name='Платное')
    booking = models.BooleanField(default=False, verbose_name='Запись')
    age = models.CharField(max_length=50, choices=AGE_CHOICES, default=ZERO, verbose_name='Возраст')
    start_time = models.TimeField(verbose_name='Время начала')
    end_time = models.TimeField(verbose_name='Время окончания')

    class Meta:
        verbose_name = 'Мероприятие Юношеская библиотека'
        verbose_name_plural = 'Мероприятия Юношеская библиотека'

    def __str__(self):
        return self.name


class WeekDB(models.Model):
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
        verbose_name = 'Расписание Детская библиотека'
        verbose_name_plural = 'Расписания Детская библиотека'

    def __str__(self):
        return self.name


class DayDB(models.Model):
    name = models.CharField(max_length=15, verbose_name='День недели')
    date = models.DateField(verbose_name='Дата', blank=True, null=True)
    week = models.ForeignKey(WeekDB, on_delete=models.CASCADE, verbose_name='Неделя', related_name='days')

    class Meta:
        verbose_name = 'Рабочий день Детская библиотека'
        verbose_name_plural = 'Рабочий день Детская библиотека'

    def __str__(self):
        return self.name


class EventyDB(models.Model):
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

    day = models.ForeignKey(DayDB, on_delete=models.CASCADE, verbose_name='День недели',
                            related_name='events')
    name = models.CharField(max_length=150, verbose_name='Название')
    payment = models.BooleanField(default=False, verbose_name='Платное')
    booking = models.BooleanField(default=False, verbose_name='Запись')
    age = models.CharField(max_length=50, choices=AGE_CHOICES, default=ZERO, verbose_name='Возраст')
    start_time = models.TimeField(verbose_name='Время начала')
    end_time = models.TimeField(verbose_name='Время окончания')

    class Meta:
        verbose_name = 'Мероприятие Детская библиотека'
        verbose_name_plural = 'Мероприятия Детская библиотека'

    def __str__(self):
        return self.name


class WeekNMB(models.Model):
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
        verbose_name = 'Расписание Новомилетская сельская библиотека'
        verbose_name_plural = 'Расписания Новомилетская сельская библиотека'

    def __str__(self):
        return self.name


class DayNMB(models.Model):
    name = models.CharField(max_length=15, verbose_name='День недели')
    date = models.DateField(verbose_name='Дата', blank=True, null=True)
    week = models.ForeignKey(WeekNMB, on_delete=models.CASCADE, verbose_name='Неделя', related_name='days')

    class Meta:
        verbose_name = 'Рабочий день Новомилетская сельская библиотека'
        verbose_name_plural = 'Рабочий день Новомилетская сельская библиотека'

    def __str__(self):
        return self.name


class EventyNMB(models.Model):
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

    day = models.ForeignKey(DayNMB, on_delete=models.CASCADE, verbose_name='День недели',
                            related_name='events')
    name = models.CharField(max_length=150, verbose_name='Название')
    payment = models.BooleanField(default=False, verbose_name='Платное')
    booking = models.BooleanField(default=False, verbose_name='Запись')
    age = models.CharField(max_length=50, choices=AGE_CHOICES, default=ZERO, verbose_name='Возраст')
    start_time = models.TimeField(verbose_name='Время начала')
    end_time = models.TimeField(verbose_name='Время окончания')

    class Meta:
        verbose_name = 'Мероприятие Новомилетская сельская библиотека'
        verbose_name_plural = 'Мероприятия Новомилетская сельская библиотека'

    def __str__(self):
        return self.name


class WeekCSB(models.Model):
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
        verbose_name = 'Расписание Черновская сельская библиотека'
        verbose_name_plural = 'Расписания Черновская сельская библиотека'

    def __str__(self):
        return self.name


class DayCSB(models.Model):
    name = models.CharField(max_length=15, verbose_name='День недели')
    date = models.DateField(verbose_name='Дата', blank=True, null=True)
    week = models.ForeignKey(WeekCSB, on_delete=models.CASCADE, verbose_name='Неделя', related_name='days')

    class Meta:
        verbose_name = 'Рабочий день Черновская сельская библиотека'
        verbose_name_plural = 'Рабочий день Черновская сельская библиотека'

    def __str__(self):
        return self.name


class EventyCSB(models.Model):
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

    day = models.ForeignKey(DayCSB, on_delete=models.CASCADE, verbose_name='День недели',
                            related_name='events')
    name = models.CharField(max_length=150, verbose_name='Название')
    payment = models.BooleanField(default=False, verbose_name='Платное')
    booking = models.BooleanField(default=False, verbose_name='Запись')
    age = models.CharField(max_length=50, choices=AGE_CHOICES, default=ZERO, verbose_name='Возраст')
    start_time = models.TimeField(verbose_name='Время начала')
    end_time = models.TimeField(verbose_name='Время окончания')

    class Meta:
        verbose_name = 'Мероприятие Черновская сельская библиотека'
        verbose_name_plural = 'Мероприятия Черновская сельская библиотека'

    def __str__(self):
        return self.name


class WeekSSB(models.Model):
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
        verbose_name = 'Расписание Соболихинская сельская библиотека'
        verbose_name_plural = 'Расписания Соболихинская сельская библиотека'

    def __str__(self):
        return self.name


class DaySSB(models.Model):
    name = models.CharField(max_length=15, verbose_name='День недели')
    date = models.DateField(verbose_name='Дата', blank=True, null=True)
    week = models.ForeignKey(WeekSSB, on_delete=models.CASCADE, verbose_name='Неделя', related_name='days')

    class Meta:
        verbose_name = 'Рабочий день Соболихинская сельская библиотека'
        verbose_name_plural = 'Рабочий день Соболихинская сельская библиотека'

    def __str__(self):
        return self.name


class EventySSB(models.Model):
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

    day = models.ForeignKey(DaySSB, on_delete=models.CASCADE, verbose_name='День недели',
                            related_name='events')
    name = models.CharField(max_length=150, verbose_name='Название')
    payment = models.BooleanField(default=False, verbose_name='Платное')
    booking = models.BooleanField(default=False, verbose_name='Запись')
    age = models.CharField(max_length=50, choices=AGE_CHOICES, default=ZERO, verbose_name='Возраст')
    start_time = models.TimeField(verbose_name='Время начала')
    end_time = models.TimeField(verbose_name='Время окончания')

    class Meta:
        verbose_name = 'Мероприятие Соболихинская сельская библиотека'
        verbose_name_plural = 'Мероприятия Соболихинская сельская библиотека'

    def __str__(self):
        return self.name


class WeekFSB(models.Model):
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
        verbose_name = 'Расписание Федурновская сельская библиотека'
        verbose_name_plural = 'Расписания Федурновская сельская библиотека'

    def __str__(self):
        return self.name


class DayFSB(models.Model):
    name = models.CharField(max_length=15, verbose_name='День недели')
    date = models.DateField(verbose_name='Дата', blank=True, null=True)
    week = models.ForeignKey(WeekFSB, on_delete=models.CASCADE, verbose_name='Неделя', related_name='days')

    class Meta:
        verbose_name = 'Рабочий день Федурновская сельская библиотека'
        verbose_name_plural = 'Рабочий день Федурновская сельская библиотека'

    def __str__(self):
        return self.name


class EventyFSB(models.Model):
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

    day = models.ForeignKey(DayFSB, on_delete=models.CASCADE, verbose_name='День недели',
                            related_name='events')
    name = models.CharField(max_length=150, verbose_name='Название')
    payment = models.BooleanField(default=False, verbose_name='Платное')
    booking = models.BooleanField(default=False, verbose_name='Запись')
    age = models.CharField(max_length=50, choices=AGE_CHOICES, default=ZERO, verbose_name='Возраст')
    start_time = models.TimeField(verbose_name='Время начала')
    end_time = models.TimeField(verbose_name='Время окончания')

    class Meta:
        verbose_name = 'Мероприятие Федурновская сельская библиотека'
        verbose_name_plural = 'Мероприятия Федурновская сельская библиотека'

    def __str__(self):
        return self.name


class WeekDBT(models.Model):
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
        verbose_name = 'Расписание Детская библиотека (Твардовского)'
        verbose_name_plural = 'Расписания Детская библиотека (Твардовского)'

    def __str__(self):
        return self.name


class DayDBT(models.Model):
    name = models.CharField(max_length=15, verbose_name='День недели')
    date = models.DateField(verbose_name='Дата', blank=True, null=True)
    week = models.ForeignKey(WeekDBT, on_delete=models.CASCADE, verbose_name='Неделя', related_name='days')

    class Meta:
        verbose_name = 'Рабочий день Детская библиотека (Твардовского)'
        verbose_name_plural = 'Рабочий день Детская библиотека (Твардовского)'

    def __str__(self):
        return self.name


class EventyDBT(models.Model):
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

    day = models.ForeignKey(DayDBT, on_delete=models.CASCADE, verbose_name='День недели',
                            related_name='events')
    name = models.CharField(max_length=150, verbose_name='Название')
    payment = models.BooleanField(default=False, verbose_name='Платное')
    booking = models.BooleanField(default=False, verbose_name='Запись')
    age = models.CharField(max_length=50, choices=AGE_CHOICES, default=ZERO, verbose_name='Возраст')
    start_time = models.TimeField(verbose_name='Время начала')
    end_time = models.TimeField(verbose_name='Время окончания')

    class Meta:
        verbose_name = 'Мероприятие Детская библиотека (Твардовского)'
        verbose_name_plural = 'Мероприятия Детская библиотека (Твардовского)'

    def __str__(self):
        return self.name


class WeekNAB(models.Model):
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
        verbose_name = 'Расписание Никольско-Архангельская библиотека'
        verbose_name_plural = 'Расписания Никольско-Архангельская библиотека'

    def __str__(self):
        return self.name


class DayNAB(models.Model):
    name = models.CharField(max_length=15, verbose_name='День недели')
    date = models.DateField(verbose_name='Дата', blank=True, null=True)
    week = models.ForeignKey(WeekNAB, on_delete=models.CASCADE, verbose_name='Неделя', related_name='days')

    class Meta:
        verbose_name = 'Рабочий день Никольско-Архангельская библиотека'
        verbose_name_plural = 'Рабочий день Никольско-Архангельская библиотека'

    def __str__(self):
        return self.name


class EventyNAB(models.Model):
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

    day = models.ForeignKey(DayNAB, on_delete=models.CASCADE, verbose_name='День недели',
                            related_name='events')
    name = models.CharField(max_length=150, verbose_name='Название')
    payment = models.BooleanField(default=False, verbose_name='Платное')
    booking = models.BooleanField(default=False, verbose_name='Запись')
    age = models.CharField(max_length=50, choices=AGE_CHOICES, default=ZERO, verbose_name='Возраст')
    start_time = models.TimeField(verbose_name='Время начала')
    end_time = models.TimeField(verbose_name='Время окончания')

    class Meta:
        verbose_name = 'Мероприятие Никольско-Архангельская библиотека'
        verbose_name_plural = 'Мероприятия Никольско-Архангельская библиотека'

    def __str__(self):
        return self.name


class WeekPPB(models.Model):
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
        verbose_name = 'Расписание Пехра-Покровская библиотека'
        verbose_name_plural = 'Расписания Пехра-Покровская библиотека'

    def __str__(self):
        return self.name


class DayPPB(models.Model):
    name = models.CharField(max_length=15, verbose_name='День недели')
    date = models.DateField(verbose_name='Дата', blank=True, null=True)
    week = models.ForeignKey(WeekPPB, on_delete=models.CASCADE, verbose_name='Неделя', related_name='days')

    class Meta:
        verbose_name = 'Рабочий день Пехра-Покровская библиотека'
        verbose_name_plural = 'Рабочий день Пехра-Покровская библиотека'

    def __str__(self):
        return self.name


class EventyPPB(models.Model):
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

    day = models.ForeignKey(DayPPB, on_delete=models.CASCADE, verbose_name='День недели',
                            related_name='events')
    name = models.CharField(max_length=150, verbose_name='Название')
    payment = models.BooleanField(default=False, verbose_name='Платное')
    booking = models.BooleanField(default=False, verbose_name='Запись')
    age = models.CharField(max_length=50, choices=AGE_CHOICES, default=ZERO, verbose_name='Возраст')
    start_time = models.TimeField(verbose_name='Время начала')
    end_time = models.TimeField(verbose_name='Время окончания')

    class Meta:
        verbose_name = 'Мероприятие Пехра-Покровская библиотека'
        verbose_name_plural = 'Мероприятия Пехра-Покровская библиотека'

    def __str__(self):
        return self.name


class WeekNB(models.Model):
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
        verbose_name = 'Расписание Никольская библиотека'
        verbose_name_plural = 'Расписания Никольская библиотека'

    def __str__(self):
        return self.name


class DayNB(models.Model):
    name = models.CharField(max_length=15, verbose_name='День недели')
    date = models.DateField(verbose_name='Дата', blank=True, null=True)
    week = models.ForeignKey(WeekNB, on_delete=models.CASCADE, verbose_name='Неделя', related_name='days')

    class Meta:
        verbose_name = 'Рабочий день Никольская библиотека'
        verbose_name_plural = 'Рабочий день Никольская библиотека'

    def __str__(self):
        return self.name


class EventyNB(models.Model):
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

    day = models.ForeignKey(DayNB, on_delete=models.CASCADE, verbose_name='День недели',
                            related_name='events')
    name = models.CharField(max_length=150, verbose_name='Название')
    payment = models.BooleanField(default=False, verbose_name='Платное')
    booking = models.BooleanField(default=False, verbose_name='Запись')
    age = models.CharField(max_length=50, choices=AGE_CHOICES, default=ZERO, verbose_name='Возраст')
    start_time = models.TimeField(verbose_name='Время начала')
    end_time = models.TimeField(verbose_name='Время окончания')

    class Meta:
        verbose_name = 'Мероприятие Никольская библиотека'
        verbose_name_plural = 'Мероприятия Никольская библиотека'

    def __str__(self):
        return self.name
















