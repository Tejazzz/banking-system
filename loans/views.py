from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from formtools.wizard.views import SessionWizardView, TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.db import transaction

from .forms import LoanForm, HomeLoanForm, EducationLoanForm, AddressForm, StudentInfoForm, UniversityForm
from .models import Insurance
from accounts.views import UserLoginView

import json

# ========================= Insurance Post API View ========================================
@csrf_exempt
def save_insurance(request):
    if request.method == 'POST':
        
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        
        insurance = Insurance()
        
        insurance.number = body.get('number')
        insurance.company = body.get('company')
        insurance.premium = body.get('premium')
        
        insurance.save()
            
        return HttpResponse(insurance.id, insurance.number)

# ========================= Home Page for loans View ========================================
def loan_application(request):
    
    context = {}
    return render(request, 'loans/loan_home.html', context)

# =========================== Personal Loan Views ===========================================
class PersonalLoanView(LoginRequiredMixin, TemplateView):
    template_name = "loans/personal_loan.html"
    
    pass
    

# =========================== Home Loan Views ===========================================
class HomeLoanFormView(LoginRequiredMixin, FormView):
    template_name = 'loans/home_loan_form.html'
    form_class = HomeLoanForm
    success_url = '/loans/home-loan-success/' # Redirect to this URL after successful form submission
    
    def get(self, request):
        ''' 
        This method is called for GET requests
        '''
        if request.user.is_authenticated:
            home_loan_form = HomeLoanForm()
            return render(request, self.template_name, {'home_loan_form': home_loan_form})

    def form_valid(self, form):
        '''
            This method is called when valid form data has been POSTed. Also redirect to success_url.
        '''
        with transaction.atomic():
            response = super().form_valid(form)
            form.save()
        return response
    
class HomeLoanSuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'loans/home_loan_success.html'
    
    def get(self, request):
        return render(request, self.template_name)
    

# =========================== Education Loan Views ========================================
class EducationLoanWizard(LoginRequiredMixin, SessionWizardView):
    template_name = 'loans/education_loan_form.html'
    form_list = [LoanForm, AddressForm, StudentInfoForm, UniversityForm, EducationLoanForm]

    def done(self, form_list, **kwargs):
        # Process the forms into models
        forms = {form.__class__.__name__: form for form in form_list}
        
        # Use similar logic from your original save method to create or update objects
        # Saving logic here...
        
        # Redirect to success page or any other
        return redirect(reverse_lazy('education_loan_success'))

    def get_context_data(self, form, **kwargs):
        context = super(EducationLoanWizard, self).get_context_data(form=form, **kwargs)
        context['step_title'] = "Step {} of {}".format(self.steps.step1, self.steps.count)
        return context


class EducationLoanFormView(LoginRequiredMixin, FormView):
    template_name = 'loans/education_loan_form.html'
    form_class = EducationLoanForm
    success_url = reverse_lazy('education_loan_success')  # Redirect to this URL after successful form submission
    
    def get(self, request):
        print("in get function")
        if request.user.is_authenticated:
            loan_form = LoanForm()
            address_form = AddressForm()
            student_info_form = StudentInfoForm()
            university_form = UniversityForm()
            education_loan_form = EducationLoanForm()
            ctx = {
                'loan_form': loan_form, 
                'education_loan_form': education_loan_form,
                'address_form': address_form,
                'student_info_form': student_info_form,
                'university_form': university_form
            }
            return render(request, self.template_name, { 'ctx': ctx})