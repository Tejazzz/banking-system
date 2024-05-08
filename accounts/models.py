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
        if self.balance > self.service_charge:  # Check to ensure balance is sufficient for deduction
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





# class BankAccountType(models.Model):
#     name = models.CharField(max_length=128)
#     maximum_withdrawal_amount = models.DecimalField(
#         decimal_places=2,
#         max_digits=12
#     )
#     annual_interest_rate = models.DecimalField(
#         validators=[MinValueValidator(0), MaxValueValidator(100)],
#         decimal_places=2,
#         max_digits=5,
#         help_text='Interest rate from 0 - 100'
#     )
#     interest_calculation_per_year = models.PositiveSmallIntegerField(
#         validators=[MinValueValidator(1), MaxValueValidator(12)],
#         help_text='The number of times interest will be calculated per year'
#     )

#     def __str__(self):
#         return self.name

#     def calculate_interest(self, principal):
#         """
#         Calculate interest for each account type.

#         This uses a basic interest calculation formula
#         """
#         p = principal
#         r = self.annual_interest_rate
#         n = Decimal(self.interest_calculation_per_year)

#         # Basic Future Value formula to calculate interest
#         interest = (p * (1 + ((r/100) / n))) - p

#         return round(interest, 2)


# class UserBankAccount(models.Model):
#     user = models.OneToOneField(
#         User,
#         related_name='account',
#         on_delete=models.CASCADE,
#     )
#     account_type = models.ForeignKey(
#         BankAccountType,
#         related_name='accounts',
#         on_delete=models.CASCADE
#     )
#     account_no = models.PositiveIntegerField(unique=True)
#     gender = models.CharField(max_length=1, choices=GENDER_CHOICE)
#     birth_date = models.DateField(null=True, blank=True)
#     balance = models.DecimalField(
#         default=0,
#         max_digits=12,
#         decimal_places=2
#     )
#     interest_start_date = models.DateField(
#         null=True, blank=True,
#         help_text=(
#             'The month number that interest calculation will start from'
#         )
#     )
#     initial_deposit_date = models.DateField(null=True, blank=True)

#     def __str__(self):
#         return str(self.account_no)

#     def get_interest_calculation_months(self):
#         """
#         List of month numbers for which the interest will be calculated

#         returns [2, 4, 6, 8, 10, 12] for every 2 months interval
#         """
#         interval = int(
#             12 / self.account_type.interest_calculation_per_year
#         )
#         start = self.interest_start_date.month
#         return [i for i in range(start, 13, interval)]
