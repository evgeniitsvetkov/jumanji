# from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.db.models import Count
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView

from vacancies.forms import ApplicationForm, CompanyForm, VacancyForm
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
            return HttpResponseRedirect(reverse('application_send', kwargs={'vacancy_id': vacancy_id}))


class ApplicationSendView(View):
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
            # Если у пользователя есть компания, то отправляем его на страницу редактирования
            if hasattr(request.user, 'company'):
                return HttpResponseRedirect('/mycompany/edit/')
            # Если компании нет, выводим приветственную страницу
            else:
                return render(request, 'mycompany/company-create.html')
        else:
            return HttpResponseRedirect('/')


class MyCompanyEditView(View):
    def get(self, request):
        if request.user.is_authenticated:
            # Если у пользователя есть компания, подтягиваем данные о ней
            if hasattr(request.user, 'company'):
                company = request.user.company
                initial_data = {"name": company.name,
                                "employee_count": company.employee_count,
                                "location": company.location,
                                "description": company.description}
                form = CompanyForm(initial=initial_data)
                return render(request, 'mycompany/company-edit.html', {'form': form})
            # Если у пользователя нет компании, выводим пустую форму
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
                # Если у пользователя уже есть компания, обновляем данные о ней
                if hasattr(request.user, 'company'):
                    company = request.user.company
                    company.name = data["name"]
                    company.employee_count = data["employee_count"]
                    company.location = data["location"]
                    company.description = data["description"]
                    company.save()
                # Если у пользователя еще нет компании, создаем ее
                else:
                    data.update({"user": request.user})
                    Company.objects.create(**data)
                return render(request, 'mycompany/company-edit.html', {'form': form})
        else:
            return HttpResponseRedirect('/')


class MyCompanyVacanciesView(View):
    def get(self, request):
        company = request.user.company
        return render(request, 'mycompany/vacancy-list.html', {'vacancies': company.vacancies.all()})


class MyCompanyVacancyCreateView(View):
    def get(self, request):
        if request.user.is_authenticated:
            form = VacancyForm()
            return render(request, 'mycompany/vacancy-edit.html', {'form': form})
        else:
            return HttpResponseRedirect('/')

    def post(self, request):
        if request.user.is_authenticated:
            form = VacancyForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                title = data["title"]
                speciality = data["speciality"]
                company = request.user.company
                skills = data["skills"]
                description = data["description"]
                salary_min = data["salary_min"]
                salary_max = data["salary_max"]
                Vacancy.objects.create(title=title,
                                       speciality=speciality,
                                       company=company,
                                       skills=skills,
                                       description=description,
                                       salary_min=salary_min,
                                       salary_max=salary_max)
            return HttpResponseRedirect('/mycompany/vacancies/')
        else:
            return HttpResponseRedirect('/')


class MyCompanyVacancyEditView(View):
    def get(self, request, vacancy_id):
        if request.user.is_authenticated:
            try:
                vacancy = Vacancy.objects.get(id=vacancy_id)
            except Vacancy.DoesNotExist:
                return HttpResponseNotFound('Вы запрашиваете несуществующую вакансию. Возможно она была удалена')

            # Если запрашиваемая вакансия принадлежит пользователю, подтягиваем данные о ней
            if request.user.company == vacancy.company:
                initial_data = {"title": vacancy.title,
                                "speciality": vacancy.speciality,
                                "skills": vacancy.skills,
                                "description": vacancy.description,
                                "salary_min": vacancy.salary_min,
                                "salary_max": vacancy.salary_max}
                form = VacancyForm(initial=initial_data)
                return render(request, 'mycompany/vacancy-edit.html', {'form': form})
            # Если запросил чужую, отправляем в раздел своих вакансий
            else:
                return HttpResponseRedirect('/mycompany/vacancies/')
        else:
            return HttpResponseRedirect('/')

    def post(self, request, vacancy_id):
        if request.user.is_authenticated:
            try:
                vacancy = Vacancy.objects.get(id=vacancy_id)
            except Vacancy.DoesNotExist:
                return HttpResponseNotFound('Вы запрашиваете несуществующую вакансию. Возможно она была удалена')

            form = VacancyForm(request.POST)
            # Если запрашиваемая вакансия принадлежит пользователю, записываем данные о ней
            if request.user.company == vacancy.company:
                if form.is_valid():
                    data = form.cleaned_data
                    vacancy.title = data["title"]
                    vacancy.speciality = data["speciality"]
                    vacancy.company = request.user.company
                    vacancy.skills = data["skills"]
                    vacancy.description = data["description"]
                    vacancy.salary_min = data["salary_min"]
                    vacancy.salary_max = data["salary_max"]
                    vacancy.save()

                    return render(request, 'mycompany/vacancy-edit.html', {'form': form})
        else:
            return HttpResponseRedirect('/')


class RegisterView(CreateView):
    form_class = UserCreationForm
    success_url = 'login'
    template_name = 'auth/register.html'


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'auth/login.html'
