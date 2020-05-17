from django.contrib.auth.models import User
from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=30)
    logo = models.CharField(max_length=200)
    description = models.TextField()
    employee_count = models.IntegerField(default=10)
    user = models.OneToOneField(User, related_name="company", on_delete=models.CASCADE, default=None, null=True)


class Speciality(models.Model):
    code = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=20)
    picture = models.CharField(max_length=200)


class Vacancy(models.Model):
    title = models.CharField(max_length=50)
    speciality = models.ForeignKey(Speciality, related_name="vacancies", on_delete=models.PROTECT)
    company = models.ForeignKey(Company, related_name="vacancies", on_delete=models.PROTECT)
    skills = models.TextField()
    description = models.TextField()
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    published_at = models.DateTimeField()


class Application(models.Model):
    written_username = models.CharField(max_length=50)
    written_phone = models.CharField(max_length=20)
    written_cover_letter = models.TextField()
    vacancy = models.ForeignKey(Vacancy, related_name="applications", on_delete=models.PROTECT)
    user = models.ForeignKey(User, related_name="applications", on_delete=models.PROTECT)