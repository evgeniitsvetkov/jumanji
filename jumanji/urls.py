"""jumanji URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path

from vacancies.views import MainView, VacanciesView, VacanciesByCategoryView, VacancyView, ApplicationSendView, \
    CompanyView, MyCompanyView, MyCompanyEditView, MyCompanyVacanciesView, MyCompanyVacancyCreateView, \
    MyCompanyVacancyEditView, RegisterView, MyLoginView

urlpatterns = [
    path('', MainView.as_view()),
    path('vacancies/', VacanciesView.as_view()),
    path('vacancies/cat/<str:category>/', VacanciesByCategoryView.as_view()),
    path('vacancies/<int:vacancy_id>/', VacancyView.as_view()),
    path('vacancies/<int:vacancy_id>/sent/', ApplicationSendView.as_view(), name='application_send'),
    path('companies/<int:company_id>/', CompanyView.as_view()),
    path('mycompany/', MyCompanyView.as_view()),
    path('mycompany/edit/', MyCompanyEditView.as_view()),
    path('mycompany/vacancies/', MyCompanyVacanciesView.as_view()),
    path('mycompany/vacancies/new/', MyCompanyVacancyCreateView.as_view()),
    path('mycompany/vacancies/<int:vacancy_id>/', MyCompanyVacancyEditView.as_view()),
    path('admin/', admin.site.urls),
    path('register/', RegisterView.as_view()),
    path('login/', MyLoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
]
