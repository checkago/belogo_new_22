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
    comment = forms.CharField(
        label='Сообщение',
        widget=forms.Textarea(attrs={'rows': '1'})
    )

    class Meta:
        model = Feedback
        fields = ('name', 'phone', 'email', 'comment', 'category')


class ServiceDopForm(forms.ModelForm):
    comment = forms.CharField(
        label='Сообщение',
        widget=forms.Textarea(attrs={'rows': '2'})
    )

    class Meta:
        model = ServiceDop
        fields = ('fio', 'service', 'date', 'phone', 'email', 'comment', 'category')