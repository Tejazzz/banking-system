from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
)
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField

import uuid


# ---------------------------- Personal Loan ---------------------------------------------
class Loan(models.Model):
    loan_id = models.BigAutoField(primary_key=True)
    amount = models.DecimalField(max_digits= 10, decimal_places=2, null=False)
    emi_amount =  models.DecimalField(max_digits= 10, decimal_places=2, null=False)
    interest_rate = models.DecimalField(decimal_places=2, max_digits=5, null=False, default=10)
    tenure = models.PositiveIntegerField(null=False)
    installment_paid = models.PositiveIntegerField(default=0, null=False)

    
# -------------------------- Home Loan ---------------------------------------------------
class Address(models.Model):
    address_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    street = models.CharField(max_length=255, null=False, blank=False)
    city = models.CharField(max_length=100, null=False, blank=False)
    state = models.CharField(max_length=100, null=False, blank=False)
    country = models.CharField(default="United States")
    zip_code = models.CharField(max_length=10, null=False, blank=False)
    
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
    
    # Foreign Key
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    
    # University Info
    name = models.CharField()
    code = models.IntegerField(unique=True)
    
    
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
    