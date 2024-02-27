from django import forms
from snowpenguin.django.recaptcha3.fields import ReCaptchaField

from web.models import Book, Question, Feedback, Bookrequest, ServiceDop


class BookForm(forms.ModelForm):
    library = forms.Select()
    comment = forms.CharField(
        label='Сообщение',
        widget=forms.Textarea(attrs={'rows': '2'})
    )

    class Meta:
        model = Book
        fields = ('library', 'age', 'school', 'fio', 'bilet', 'phone', 'email', 'comment', 'agreement')


class QuestionForm(forms.ModelForm):
    comment = forms.CharField(
        label='Сообщение',
        widget=forms.Textarea(attrs={'rows': '2'})
    )

    class Meta:
        model = Question
        fields = ('name', 'email', 'phone', 'comment', 'category', 'agreement')


class FeedbackForm(forms.ModelForm):
    comment = forms.CharField(
        label='Сообщение',
        widget=forms.Textarea(attrs={'rows': '1'})
    )
    email = forms.EmailField(required=False, widget=forms.EmailInput)
    # captcha = ReCaptchaField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Имя'
        self.fields['phone'].label = 'Номер телефона'
        self.fields['email'].label = 'E-mail'
        self.fields['comment'].label = 'Коментарий'
        self.fields['agreement'].label = 'Согласие'

    def clean_email(self):
        email = self.cleaned_data['email']
        domain = email.split('.')[-1]
        if domain in ['com', 'net', 'org', 'xyz', 'de', 'fr', 'ua', 'nl', 'cz', 'group', 'biz', 'dk']:
            raise forms.ValidationError(f'Использование почтового ящика в домене .{domain} заблокированно')
        return email

    class Meta:
        model = Feedback
        fields = ('name', 'phone', 'email', 'comment', 'agreement')


class BookrequestForm(forms.ModelForm):
    comment = forms.CharField(
        label='Список книг',
        widget=forms.Textarea(attrs={'rows': '4'})
    )

    class Meta:
        model = Bookrequest
        fields = ('name', 'email', 'comment', 'agreement')


class ServiceDopForm(forms.ModelForm):
    comment = forms.CharField(
        label='Ваше сообщение',
        widget=forms.Textarea(attrs={'rows': '5'})
    )
    class Meta:
        model = ServiceDop
        fields = ('date', 'fio', 'phone', 'email', 'comment', 'file', 'agreement')

