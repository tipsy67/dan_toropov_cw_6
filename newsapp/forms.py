from django import forms
from django.forms import CheckboxSelectMultiple

from newsapp.models import NewsLetter, Client, Message


# class DateTimePicker(forms.DateTimeInput):
#     input_type = 'datetime-local'


class NewsLetterForm (forms.ModelForm):
    # first_mailing_at = forms.DateTimeField(label='Первая отправка')

    class Meta:
        model = NewsLetter
        exclude = ('status','owner')
        widgets = {
            'first_mailing_at': forms.DateTimeInput(format='%Y-%m-%dT%H:%M', attrs={'type': 'datetime-local'}),
            # 'first_mailing_at': DateTimePicker(),
            'clients':CheckboxSelectMultiple
        }


    def __init__(self, *args, **kwargs):
        super(NewsLetterForm, self).__init__(*args, **kwargs)
        owner = kwargs['instance'].owner
        self.fields['clients'].queryset = Client.objects.filter(owner=owner)
        self.fields['message'].queryset = Message.objects.filter(owner=owner)

