from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Company(models.Model):
    name = models.CharField("Название комапнии", max_length=100)
    location = models.CharField("География", max_length=30)
    logo = models.CharField(max_length=200)
    description = models.TextField("Информация о компании")
    employee_count = models.IntegerField("Количество человек в компании", default=10)
    user = models.OneToOneField(User, related_name="company", on_delete=models.CASCADE, default=None, null=True)


class Speciality(models.Model):
    code = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=20)
    picture = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Vacancy(models.Model):
    title = models.CharField("Название вакансии", max_length=50)
    speciality = models.ForeignKey(Speciality, related_name="vacancies", on_delete=models.PROTECT)
    company = models.ForeignKey(Company, related_name="vacancies", on_delete=models.PROTECT)
    skills = models.TextField("Требуемые навыки")
    description = models.TextField("Описание вакансии")
    salary_min = models.IntegerField("Зарплата от")
    salary_max = models.IntegerField("Зарплата до")
    published_at = models.DateTimeField(default=timezone.now)


class Application(models.Model):
    written_username = models.CharField("Имя", max_length=50)
    written_phone = models.CharField("Телефон для связи", max_length=20)
    written_cover_letter = models.TextField("Сопроводительное письмо")
    vacancy = models.ForeignKey(Vacancy, related_name="applications", on_delete=models.PROTECT)
    user = models.ForeignKey(User, related_name="applications", on_delete=models.PROTECT)
