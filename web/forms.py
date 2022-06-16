from django import forms
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class BookForm(forms.ModelForm):
    library = forms.Select()
    comment = forms.CharField(
        label='Сообщение',
        widget=forms.Textarea(attrs={'rows': '2'})
    )

    class Meta:
        model = Book
        fields = ('library', 'fio', 'bilet', 'phone', 'email', 'comment', 'category')


class QuestionForm(forms.ModelForm):
    comment = forms.CharField(
        label='Сообщение',
        widget=forms.Textarea(attrs={'rows': '2'})
    )

    class Meta:
        model = Question
        fields = ('name', 'email', 'phone', 'comment', 'category')


class FeedbackForm(forms.ModelForm):
    text = forms.CharField(
        label='Сообщение',
        widget=forms.Textarea(attrs={'rows': '1'})
    )
    email = forms.EmailField(required=False, widget=forms.EmailInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Имя'
        self.fields['phone'].label = 'Номер телефона'
        self.fields['email'].label = 'E-mail'
        self.fields['comment'].label = 'Коментарий'

    def clean_email(self):
        email = self.cleaned_data['email']
        domain = email.split('.')[-1]
        if domain in ['com', 'net', 'org', 'xyz', 'de', 'fr', 'ua', 'nl', 'cz', 'group', 'biz', 'dk']:
            raise forms.ValidationError(f'Использование почтового ящика в домене .{domain} заблокированно')
        return email

    class Meta:
        model = Feedback
        fields = ('name', 'phone', 'email', 'comment')


class ServiceDopForm(forms.ModelForm):
    comment = forms.CharField(
        label='Сообщение',
        widget=forms.Textarea(attrs={'rows': '2'})
    )

    class Meta:
        model = ServiceDop
        fields = ('fio', 'service', 'date', 'phone', 'email', 'comment', 'category')