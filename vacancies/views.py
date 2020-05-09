from django.shortcuts import render
from django.views import View

from vacancies.models import Company, Speciality


class MainView(View):
    def get(self, request):
        specialties = Speciality.objects.all()
        companies = Company.objects.all()

        return render(request, 'vacancies/index.html', {'specialties': specialties,
                                                        'companies': companies})


class VacanciesView(View):
    def get(self, request):
        return render(request, 'vacancies/vacancies.html')


class VacanciesByCategoryView(View):
    def get(self, request, category):
        return render(request, 'vacancies/vacancies.html')


class VacancyView(View):
    def get(self, request, vacancy_id):
        return render(request, 'vacancies/vacancy.html')


class CompanyView(View):
    def get(self, request, company_id):
        return render(request, 'vacancies/company.html')
