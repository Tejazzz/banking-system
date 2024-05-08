import logging
from decimal import Decimal, getcontext

from django import forms
from django.db import transaction
from django.forms import ModelForm
from django.forms.widgets import NumberInput

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

                # Calculate EMI
                amount = self.cleaned_data['amount']
                tenure = self.cleaned_data['tenure']
                interest_rate = Decimal('0.10')  # 10% annual interest rate
                
                amount = Decimal(amount)
                tenure = Decimal(tenure)
                
                
                getcontext().prec = 10
                monthly_interest_rate = interest_rate / 12
                number_of_payments = tenure  # tenure in months
                emi_amount = (amount * monthly_interest_rate * (Decimal('1') + monthly_interest_rate) ** number_of_payments) / \
                                ((Decimal('1') + monthly_interest_rate) ** number_of_payments - Decimal('1'))

                # Output the EMI rounded to two decimal places
                emi_amount = emi_amount.quantize(Decimal('1.00'), rounding='ROUND_HALF_UP')

                print(emi_amount)
                home_loan.emi_amount = emi_amount

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
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    graduation_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

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

        education_loan = super().save(commit=False)  # Do not commit yet
        try:
            with transaction.atomic():  # Use atomic to ensure all or nothing is saved
                # Create or update the student information

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

                # Set additional fields
                education_loan.university = self.cleaned_data['university']
                education_loan.graduation_date = self.cleaned_data['graduation_date']
                education_loan.degree = self.cleaned_data['degree']
                education_loan.college_id = self.cleaned_data['college_id']

                # Assuming `amount` and `tenure` are part of EducationLoan model or form
                amount = self.cleaned_data.get('amount')
                tenure = self.cleaned_data.get('tenure')
                interest_rate = Decimal('0.08')  # Assuming interest rate is fixed for simplification

                # Calculate EMI
                getcontext().prec = 10
                monthly_interest_rate = interest_rate / 12
                number_of_payments = tenure * 12  # assuming tenure is in years

                emi_amount = (Decimal(amount) * monthly_interest_rate * (
                        Decimal('1') + monthly_interest_rate) ** number_of_payments) / \
                             ((Decimal('1') + monthly_interest_rate) ** number_of_payments - Decimal('1'))

                education_loan.emi_amount = emi_amount.quantize(Decimal('1.00')) if emi_amount <= Decimal(
                    '99999999.99') else Decimal('99999999.99')

                education_loan.save()  # Now commit the saved loan

        except Exception as e:
            logging.error(f"Failed to save Education Loan form: {e}")
            self.add_error(None, f"Failed to process the form due to a system error: {e}")
            raise

        return education_loan
