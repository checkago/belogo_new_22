from django import forms
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ('fio', 'bilet', 'phone', 'email', 'comment', 'category')


class FeedbackForm(forms.ModelForm):
    comment = forms.CharField(
        label='Сообщение',
        widget=forms.Textarea(attrs={'rows': '1'})
    )

    class Meta:
        model = Feedback
        fields = ('name', 'phone', 'email', 'comment', 'category')