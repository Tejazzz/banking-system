from django import forms
from django.db import transaction, IntegrityError
from django.forms.widgets import SelectDateWidget, NumberInput
from django.core.exceptions import ValidationError
from decimal import Decimal, getcontext

from .models import Address, Loan, HomeLoan, EducationLoan, StudentInfo, University, Insurance
from .constants import US_STATES

class LoanForm(forms.ModelForm):
    
    class Meta:
        model = Loan
        fields = [
            'amount',
            'tenure'
        ]
        
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
        
    def save(self, commit=True):
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

                # Calculate EMI
                amount = self.cleaned_data['amount']
                tenure = self.cleaned_data['tenure']
                interest_rate = Decimal('0.10')  # 10% annual interest rate
                monthly_interest_rate = interest_rate / 12
                number_of_payments = tenure * 12  # converting years to months

                # EMI Formula: E = [P * r * (1+r)^n] / [(1+r)^n – 1]
                getcontext().prec = 10  
                emi_amount = (Decimal(amount) * monthly_interest_rate * (Decimal('1') + monthly_interest_rate) ** number_of_payments) / \
                    ((Decimal('1') + monthly_interest_rate) ** number_of_payments - Decimal('1'))
                if emi_amount.quantize(Decimal('1.00')) > Decimal('99999999.99'):
                    # Handle overflow or adjust precision/scale
                    emi_amount = Decimal('99999999.99')

                home_loan.emi_amount = round(emi_amount, 2)

                # Save HomeLoan to the DB if commit is True
                if commit:
                    home_loan.save()
                return home_loan
        # Handle specific errors with decimal conversion or arithmetic
        except ValueError as ve:
            raise ValidationError({"amount": "Invalid number input or arithmetic issue: " + str(ve)})
        except IntegrityError as ie:
            raise ValidationError({"database": "Database integrity error: " + str(ie)})
        except Exception as e:
            raise ValidationError({"general": "An error occurred: " + str(e)})

# =============================== Education Loan Forms ============================================

class UniversityForm(forms.ModelForm):
    class Meta:
        model = University 
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class StudentInfoForm(forms.ModelForm):
    date_of_birth = forms.DateTimeField(label="Date of Birth", required=True, widget=NumberInput(attrs={'type':'date'}))
    class Meta:
        model = StudentInfo
        fields = '__all__'
            
        


class EducationLoanForm(forms.ModelForm):
    graduation_date = forms.DateTimeField(label="Graduation Date", required=True, widget=NumberInput(attrs={'type':'date'}))
    class Meta:
        model = EducationLoan
        fields = get_fields(LoanForm.Meta) + get_fields(UniversityForm.Meta) + get_fields(AddressForm) + get_fields(StudentInfoForm.Meta) + ['graduation_date', 'degree', 'college_id']
    
    
    def __init__(self, *args, **kwargs):
        super(EducationLoanForm, self).__init__(*args, **kwargs)
        self.fields.update(LoanForm.base_fields)
        self.fields.update(UniversityForm.base_fields)
        self.fields.update(StudentInfoForm.base_fields)
        # Ensure all fields are properly initialized here
        
    def save(self, commit=True):
        with transaction.atomic():
            # Manually handle data for University and StudentInfo
            university_data = {
                'name': self.cleaned_data.get('university_name'),
                'code': self.cleaned_data.get('university_code')
            }
            university, created = University.objects.update_or_create(
                name=university_data['name'],
                defaults=university_data
            )

            student_info_data = {
                'first_name': self.cleaned_data.get('student_first_name'),
                'last_name': self.cleaned_data.get('student_last_name'),
                'date_of_birth': self.cleaned_data.get('student_date_of_birth'),
                'email': self.cleaned_data.get('student_email'),
                'phone': self.cleaned_data.get('student_phone')
            }
            student_info, created = StudentInfo.objects.update_or_create(
                email=student_info_data['email'],  # assuming email is unique
                defaults=student_info_data
            )

            # Assign related objects to the EducationLoan instance
            education_loan = super(EducationLoanForm, self).save(commit=False)
            education_loan.university = university
            education_loan.student_info = student_info
            education_loan.graduation_date = self.cleaned_data['graduation_date']
            education_loan.degree = self.cleaned_data['degree']
            education_loan.college_id = self.cleaned_data['college_id']

            if commit:
                education_loan.save()

            return education_loan

# ------------------------- Unused Forms ------------------------------

# class EducationLoanForm(LoanForm, UniversityForm, StudentInfoForm):
    
#     class Meta(LoanForm.Meta, UniversityForm.Meta, StudentInfoForm.Meta):
#         model = EducationLoan
#         print(LoanForm.Meta.fields)
#         fields = [LoanForm.Meta.fields] + [StudentInfoForm.Meta.fields] + [UniversityForm.Meta.fields] + ['graduation_date', 'degree', 'college_id']


#     # def save(self, commit=True):
#     #     university = University(name=self.cleaned_data)


# class EducationLoan(forms.ModelForm):
#     class Meta:
#         model = EducationLoan
#         fields = ['graduation_date', 'degree', 'college_id']


# class EducationLoanForm(forms.ModelForm):
#     # Fields from University
#     university_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
#     university_code = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    
#     # Fields from StudentInfo
#     student_first_name = forms.CharField()
#     student_middle_name = forms.CharField(required=False)
#     student_last_name = forms.CharField()
#     student_date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
#     student_email = forms.EmailField()
#     student_phone = forms.CharField()
    
#     # Specific fields for EducationLoan
#     graduation_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
#     degree = forms.CharField()
#     college_id = forms.CharField()

#     class Meta:
#         model = EducationLoan
#         fields = ['graduation_date', 'degree', 'college_id']

#     def save(self, commit=True):
#         # This needs to be implemented based on how you handle related objects
#         # This is a simplified approach:
#         university = University(name=self.cleaned_data['university_name'], code=self.cleaned_data['university_code'])
#         university.save()

#         student_info = StudentInfo(
#             first_name=self.cleaned_data['student_first_name'],
#             middle_name=self.cleaned_data['student_middle_name'],
#             last_name=self.cleaned_data['student_last_name'],
#             date_of_birth=self.cleaned_data['student_date_of_birth'],
#             email=self.cleaned_data['student_email'],
#             phone=self.cleaned_data['student_phone']
#         )
#         student_info.save()

#         education_loan = super().save(commit=False)
#         education_loan.university = university
#         education_loan.student_info = student_info
#         if commit:
#             education_loan.save()
#         return education_loan