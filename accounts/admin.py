from django.contrib import admin

from .models import User, UserAddress, CheckingBankAccount, SavingsBankAccount

admin.site.register(User)
admin.site.register(UserAddress)
admin.site.register(CheckingBankAccount)
admin.site.register(SavingsBankAccount)
