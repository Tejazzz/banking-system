import uuid
from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Max
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


# ---------------------------- Personal Loan ---------------------------------------------
class Loan(models.Model):
    class LoanStatusChoices(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        APPROVED = 'Approved', 'Approved'
        DECLINED = 'Declined', 'Declined'

    LOAN_TYPES = (
        ('personal', 'Personal Loan'),
        ('home', 'Home Loan'),
        ('education', 'Education Loan')
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    loan_id = models.BigAutoField(primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    emi_amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    interest_rate = models.DecimalField(decimal_places=2, max_digits=5, null=False, default=10)
    tenure = models.PositiveIntegerField(null=False)
    installment_paid = models.PositiveIntegerField(default=0, null=False)
    status = models.CharField(
        max_length=10,
        choices=LoanStatusChoices.choices,
        default=LoanStatusChoices.PENDING,
        null=False
    )
    loan_type = models.CharField(choices=LOAN_TYPES, max_length=10, default='personal')
    
    class Meta:
        unique_together = ('user', 'loan_type')

    def save(self, *args, **kwargs):
        self.calculate_emi()
        super().save(*args, **kwargs)

    def calculate_emi(self):
        P = self.amount
        r = self.interest_rate / Decimal('100.0') / Decimal('12.0')
        n = self.tenure * 12  # Convert tenure to months

        if n > 0 and r > 0:
            emi = (P * r * (1 + r) ** n) / ((1 + r) ** n - 1)
        else:
            emi = 0

        self.emi_amount = emi.quantize(Decimal('0.01'))

    # -------------------------- Home Loan ---------------------------------------------------


class Address(models.Model):
    address_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    street = models.CharField(max_length=255, null=False, blank=False)
    city = models.CharField(max_length=100, null=False, blank=False)
    state = models.CharField(max_length=100, null=False, blank=False)
    country = models.CharField(default="United States")
    zip_code = models.CharField(max_length=10, null=False, blank=False)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state}, {self.country}, {self.zip_code}"


class Insurance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    number = models.IntegerField(null=False, blank=False)
    company = models.CharField(max_length=255)
    premium = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.company} - ${self.premium}"


# year validator
def validate_year(value):
    current_year = timezone.now().year
    if value > current_year:
        raise ValidationError(f'Year {value} is in the future.')
    if value < 1800:  # Assuming houses built before 1800 are not considered
        raise ValidationError(f'Year {value} is too far in the past.')


class HomeLoan(Loan):
    home_address = models.OneToOneField(Address, on_delete=models.CASCADE, related_name='home_loans')
    insurance = models.OneToOneField(Insurance, on_delete=models.CASCADE)
    house_built_year = models.PositiveIntegerField(validators=[validate_year])


# ------------------------------- Student Loan ---------------------------------------
class University(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # University Info
    name = models.CharField()
    code = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.code:  # Check if code is not already set
            last_code = University.objects.aggregate(Max('code'))['code__max']
            self.code = last_code + 1 if last_code else 1001  # Start from 1001 if no entries exist
        super(University, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class StudentInfo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    first_name = models.CharField()
    middle_name = models.CharField(null=True)
    last_name = models.CharField()
    date_of_birth = models.DateField()
    email = models.EmailField(unique=True)
    phone = PhoneNumberField()


class EducationLoan(Loan):
    university = models.OneToOneField(University, on_delete=models.CASCADE)
    student_info = models.OneToOneField(StudentInfo, on_delete=models.CASCADE)

    graduation_date = models.DateField()
    degree = models.CharField()
    college_id = models.CharField()

    def __init__(self, *args, **kwargs):
        super(EducationLoan, self).__init__(*args, **kwargs)
        if self._state.adding:
            self.interest_rate = Decimal('8.0')
