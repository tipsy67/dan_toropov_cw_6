from datetime import datetime

from django import forms
from django.forms import SplitDateTimeWidget, DateTimeInput, CheckboxSelectMultiple
from django.contrib.admin import widgets
from newsapp.models import NewsLetter

# class DateTimePicker(forms.DateTimeInput):
#     input_type = 'datetime-local'


class NewsLetterForm (forms.ModelForm):
    # first_mailing_at = forms.DateTimeField(label='Первая отправка')

    class Meta:
        model = NewsLetter
        exclude = ('status',)
        widgets = {
            'first_mailing_at': forms.DateTimeInput(format=('%Y-%m-%dT%H:%M'), attrs={'type': 'datetime-local'}),
            # 'first_mailing_at': DateTimePicker(),
            'clients':CheckboxSelectMultiple
        }

