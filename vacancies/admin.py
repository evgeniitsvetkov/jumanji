from django.contrib import admin

from vacancies.models import Vacancy, Company, Application


class VacancyAdmin(admin.ModelAdmin):
    pass


class CompanyAdmin(admin.ModelAdmin):
    pass


class ApplicationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Vacancy, VacancyAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Application, ApplicationAdmin)
