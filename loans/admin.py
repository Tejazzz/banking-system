# Register your models here.
from django.contrib import admin

from loans import models

admin.site.register(models.Loan)
admin.site.register(models.HomeLoan)
admin.site.register(models.EducationLoan)
admin.site.register(models.Address)
admin.site.register(models.StudentInfo)
