from django import forms
from django.db import transaction
from django.forms import ModelForm
from django.forms.widgets import NumberInput
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

import logging

from .constants import US_STATES
from .models import Address, Loan, HomeLoan, EducationLoan, StudentInfo, University, Insurance


class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['amount', 'tenure']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Extract user from kwargs and remove it
        super(LoanForm, self).__init__(*args, **kwargs)

    def save(self, user=None, commit=True):
        loan = super(LoanForm, self).save(commit=False)
        loan.loan_type = 'personal'
        # Optionally perform other custom logic before saving
        if self.user:
            loan.user = self.user
        if commit:
            loan.save()
        return loan


# Utility Function to extract list of fields from Form Classs
def get_fields(form_meta):
    if hasattr(form_meta, 'fields'):
        if form_meta.fields == '__all__':
            return []
        return list(form_meta.fields)
    return []


# =============================== Home Loan Forms ============================================

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'


class HomeLoanForm(forms.ModelForm):
    # Fields from Address model
    street = forms.CharField(max_length=255)
    city = forms.CharField(max_length=100)
    state = forms.ChoiceField(choices=US_STATES)
    zip_code = forms.CharField(max_length=10)

    insurance = forms.ModelChoiceField(queryset=Insurance.objects.all(), empty_label="Select Insurance")

    class Meta:
        model = HomeLoan
        fields = get_fields(LoanForm.Meta) + ['house_built_year', 'insurance']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Extract user from kwargs and remove it
        super(HomeLoanForm, self).__init__(*args, **kwargs)

    def save(self, commit=True, user=None):
        try:
            with transaction.atomic():
                # Creating the address object
                address = Address.objects.create(
                    street=self.cleaned_data['street'],
                    city=self.cleaned_data['city'],
                    state=self.cleaned_data['state'],
                    zip_code=self.cleaned_data['zip_code']
                )

                # Getting insurance data
                insurance = self.cleaned_data['insurance']

                # Saving the HomeLoan without committing to DB yet
                home_loan = super().save(commit=False)
                home_loan.home_address = address
                home_loan.insurance = insurance
                home_loan.loan_type = 'home'

                if self.user:
                    home_loan.user = self.user

                if commit:
                    home_loan.save()
                return home_loan
        except Exception as e:
            logging.error(f"Failed to save Home Loan form: {e}")
            self.add_error(None, f"Failed to process the form due to a system error: {e}")


# =============================== Education Loan Forms ============================================
class StudentInfoForm(forms.ModelForm):
    date_of_birth = forms.DateTimeField(label="Date of Birth", required=True,
                                        widget=NumberInput(attrs={'type': 'date'}))

    class Meta:
        model = StudentInfo
        fields = '__all__'


def validate_age(value):
    """ Validator to check if age is at least 16 years """
    today = timezone.now().date()
    age_16 = today - timedelta(days=16*365.25)  # Approximation including leap years
    if value > age_16:
        raise ValidationError("Student must be at least 16 years old.")

def validate_graduation(value):
    """ Validator to check if the graduation date is at least one year from today """
    min_graduation_date = timezone.now().date() + timedelta(days=365)
    if value < min_graduation_date:
        raise ValidationError("Graduation date must be at least one year from today.")
    

class EducationLoanForm(ModelForm):
    university = forms.ModelChoiceField(
        queryset=University.objects.all().order_by('name'),
        empty_label="Select University",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), validators=[validate_age])
    graduation_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), validators=[validate_graduation])

    class Meta:
        model = EducationLoan
        fields = get_fields(LoanForm.Meta) + ['university', 'graduation_date', 'degree', 'college_id', 'first_name',
                                              'last_name', 'email', 'phone', 'date_of_birth']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(EducationLoanForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        if not commit:
            raise ValueError("Cannot save without committing the transaction")

        education_loan = super().save(commit=False) 
        try:
            with transaction.atomic():
        
                education_loan.loan_type = 'education'

                student = StudentInfo.objects.create(
                    first_name=self.cleaned_data['first_name'],
                    last_name=self.cleaned_data['last_name'],
                    date_of_birth=self.cleaned_data['date_of_birth'],
                    email=self.cleaned_data['email'],
                    phone=self.cleaned_data['phone']
                )

                education_loan.student_info = student
                if hasattr(self, 'user') and self.user:
                    education_loan.user = self.user

                education_loan.university = self.cleaned_data['university']
                education_loan.graduation_date = self.cleaned_data['graduation_date']
                education_loan.degree = self.cleaned_data['degree']
                education_loan.college_id = self.cleaned_data['college_id']

                education_loan.save()  # Now commit the saved loan

        except Exception as e:
            logging.error(f"Failed to save Education Loan form: {e}")
            self.add_error(None, f"Failed to process the form due to a system error: {e}")
            raise

        return education_loan
