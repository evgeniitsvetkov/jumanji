from django import forms
from django.forms import ModelForm

from vacancies.models import Application


class VacancyForm(forms.Form):
    user_name = forms.CharField(label='Вас зовут', max_length=100)
    user_phone = forms.CharField(label='Ваш телефон', max_length=20)
    user_msg = forms.CharField(label="Сопроводительное письмо", widget=forms.Textarea)


class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        fields = ['written_username', 'written_phone', 'written_cover_letter']



