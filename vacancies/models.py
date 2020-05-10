from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=30)
    logo = models.CharField(max_length=200)
    description = models.TextField()
    employee_count = models.IntegerField(default=10)


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
