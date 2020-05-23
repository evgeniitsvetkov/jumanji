from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.db.models import Count
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView

from vacancies.forms import ApplicationForm, CompanyForm
from vacancies.models import Company, Speciality, Vacancy


class MainView(View):
    def get(self, request):
        specialties = Speciality.objects.annotate(count=Count('vacancies'))
        companies = Company.objects.annotate(count=Count('vacancies'))
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

        form = ApplicationForm()
        return render(request, 'vacancies/vacancy.html', {'vacancy': vacancy,
                                                          'form': form})

    def post(self, request, vacancy_id):
        form = ApplicationForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(reverse('application_sent', kwargs={'vacancy_id': vacancy_id}))


class ApplicationSentView(View):
    def get(self, request, vacancy_id):
        return render(request, 'vacancies/sent.html', {'vacancy_id': vacancy_id})


class CompanyView(View):
    def get(self, request, company_id):
        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            return HttpResponseNotFound('Вы запрашиваете несуществующую компанию')

        return render(request, 'vacancies/company.html', {'company': company,
                                                          'vacancies': company.vacancies.all()})


class MyCompanyView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if hasattr(request.user, 'company'):
                return HttpResponseRedirect('/mycompany/edit/')
            else:
                return render(request, 'mycompany/company-create.html')
        else:
            return HttpResponseRedirect('/')


class MyCompanyEditView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if hasattr(request.user, 'company'):
                company = request.user.company
                initial_data = {"name": company.name,
                                "employee_count": company.employee_count,
                                "location": company.location,
                                "description": company.description}
                form = CompanyForm(initial=initial_data)
                return render(request, 'mycompany/company-edit.html', {'form': form})
            else:
                form = CompanyForm()
                return render(request, 'mycompany/company-edit.html', {'form': form})
        else:
            return HttpResponseRedirect('/')

    def post(self, request):
        if request.user.is_authenticated:
            form = CompanyForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                data.update({"user": request.user})
                Company.objects.create(**data)
                return render(request, 'mycompany/company-edit.html', {'form': form})
        else:
            return HttpResponseRedirect('/')


class RegisterView(CreateView):
    form_class = UserCreationForm
    success_url = 'login'
    template_name = 'auth/register.html'


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'auth/login.html'
