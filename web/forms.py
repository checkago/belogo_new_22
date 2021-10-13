from django import forms
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ('fio', 'bilet', 'phone', 'email', 'comment', 'category')