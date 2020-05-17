from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.views import View

from vacancies.models import Company, Speciality, Vacancy


class MainView(View):
    def get(self, request):
        specialties = Speciality.objects.all()
        companies = Company.objects.all()

        return render(request, 'vacancies/index.html', {'specialties': specialties,
                                                        'companies': companies})


class VacanciesView(View):
    def get(self, request):
        vacancies = Vacancy.objects.all()

        return render(request, 'vacancies/vacancies.html', {'vacancies': vacancies,
                                                            'page_title': 'Все вакансии'})


class VacanciesByCategoryView(View):
    def get(self, request, category):
        try:
            category = Speciality.objects.get(code=category)
        except Speciality.DoesNotExist:
            return HttpResponseNotFound('Вы запрашиваете несуществующую специализацию')

        return render(request, 'vacancies/vacancies.html', {'vacancies': category.vacancies.all(),
                                                            'page_title': category.title})


class VacancyView(View):
    def get(self, request, vacancy_id):
        try:
            vacancy = Vacancy.objects.get(id=vacancy_id)
        except Vacancy.DoesNotExist:
            return HttpResponseNotFound('Вы запрашиваете несуществующую вакансию. Возможно она была удалена')

        return render(request, 'vacancies/vacancy.html', {'vacancy': vacancy})


class CompanyView(View):
    def get(self, request, company_id):
        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            return HttpResponseNotFound('Вы запрашиваете несуществующую компанию')

        return render(request, 'vacancies/company.html', {'company': company,
                                                          'vacancies': company.vacancies.all()})
