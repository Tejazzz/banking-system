from django.contrib import admin

from .models import User, UserAddress, CheckingBankAccount, SavingsBankAccount, BankAccount

admin.site.register(User)
admin.site.register(BankAccount)
admin.site.register(CheckingBankAccount)
admin.site.register(SavingsBankAccount)
