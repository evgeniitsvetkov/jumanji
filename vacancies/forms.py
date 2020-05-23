# from django import forms
from django.forms import ModelForm

from vacancies.models import Application, Company, Vacancy


# class ApplicationForm(forms.Form):
#     user_name = forms.CharField(label='Вас зовут', max_length=100)
#     user_phone = forms.CharField(label='Ваш телефон', max_length=20)
#     user_msg = forms.CharField(label="Сопроводительное письмо", widget=forms.Textarea)


class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        fields = ['written_username', 'written_phone', 'written_cover_letter']


class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'location', 'description', 'employee_count']


class VacancyForm(ModelForm):
    class Meta:
        model = Vacancy
        fields = ['title', 'speciality', 'salary_min', 'salary_max', 'skills', 'description']
