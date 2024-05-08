from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from decimal import Decimal

from .constants import ACCOUNT_TYPES
from .managers import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, null=False, blank=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    @property
    def balance(self):
        if hasattr(self, 'account'):
            return self.account.balance
        return 0


class UserAddress(models.Model):
    user = models.OneToOneField(
        User,
        related_name='address',
        on_delete=models.CASCADE,
    )
    street_address = models.CharField(max_length=512)
    city = models.CharField(max_length=256)
    postal_code = models.PositiveIntegerField()
    country = models.CharField(max_length=256)

    def __str__(self):
        return self.user.email


# ==================================== Bank Accounts =========================================
class BankAccount(models.Model):
    user = models.ForeignKey(User, related_name='account', on_delete=models.CASCADE)
    account_no = models.BigAutoField(primary_key=True, unique=True)
    date_opened = models.DateField(default=timezone.now)
    balance = models.DecimalField(
        default=0.00,
        max_digits=12,
        decimal_places=2
    )
    account_type = models.CharField(choices=ACCOUNT_TYPES, default='CHECKING')


class CheckingBankAccount(BankAccount):
    service_charge = models.DecimalField(
        default=10.00,
        max_digits=12,
        decimal_places=2
    )

    def deduct_service_charge(self):
        '''Deducts service charge from the account balance and returns the deducted amount.'''
        if self.balance > self.service_charge:  
            self.balance -= self.service_charge
            self.save()
            return self.service_charge
        return Decimal('0.00')


class SavingsBankAccount(BankAccount):
    interest_rate = models.DecimalField(
        default=8,
        max_digits=5,
        decimal_places=2,
        help_text="Annual interest rate in percentage"
    )

    def add_interest(self):
        '''Adds interest to the account balance based on the interest rate and returns the interest amount.'''
        
        monthly_interest_rate = self.interest_rate / 12 / 100
        interest_amount = monthly_interest_rate * self.balance
        self.balance += interest_amount
        self.save()
        return interest_amount