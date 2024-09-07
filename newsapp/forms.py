from datetime import datetime

from django import forms
from django.forms import SplitDateTimeWidget, DateTimeInput, CheckboxSelectMultiple

from newsapp.models import NewsLetter


class NewsLetterForm (forms.ModelForm):
    first_mailing_at = forms.DateTimeField(label='Первая отправка')

    class Meta:
        model = NewsLetter
        exclude = ('status',)
        widgets = {
            'first_mailing_at': DateTimeInput(),
            'clients':CheckboxSelectMultiple
        }

