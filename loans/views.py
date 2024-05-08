import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction, IntegrityError
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, UpdateView
from django.views.generic.edit import FormView

from .forms import LoanForm, HomeLoanForm, EducationLoanForm
from .models import Insurance, Loan, University


# ========================= Home Page for loans View ========================================
def loan_application(request):
    context = {}
    return render(request, 'loans/loans_apply.html', context)


# =========================== Personal Loan Views ===========================================
# class PersonalLoanCreateView(LoginRequiredMixin, CreateView):
#     model = Loan
#     form_class = LoanForm
#     template_name = 'loans/personal_loan_form.html'
#     success_url = reverse_lazy('loans:loan_home')  # Redirect to loan list view after a loan is successfully created

#     def get(self, request):
#         '''
#         This method is called for GET requests
#         '''
#         if request.user.is_authenticated:
#             personal_loan_form = LoanForm()
#             return render(request, self.template_name, {'personal_loan_form': personal_loan_form})

#     def form_valid(self, form):
#         '''
#         This method is called when valid form data has been posted.
#         It should return an HttpResponse.
#         '''
#         messages.success(self.request, "Personal loan application submitted successfully!")
#         with transaction.atomic():
#             form.instance.user = self.request.user
#             return super().form_valid(form)  # Saves the form instance, form.save() is called here

#     def form_invalid(self, form):
#         ''' Adding an error message '''
#         messages.error(self.request, "Error submitting the personal loan application. Please check the form.")
#         return super().form_invalid(form)

#     def get_form_kwargs(self):
#         """
#         Pass additional kwargs to the form instance. Useful for passing the request object or other variables.
#         """
#         kwargs = super(PersonalLoanCreateView, self).get_form_kwargs()
#         kwargs['user'] = self.request.user
#         return kwargs

class PersonalLoanCreateView(LoginRequiredMixin, CreateView):
    model = Loan
    form_class = LoanForm
    template_name = 'loans/personal_loan_form.html'
    success_url = reverse_lazy('loans:loan_home')  # Redirect to loan list view after a loan is successfully created

    def get(self, request):
        '''
        This method is called for GET requests
        '''
        personal_loan_form = LoanForm()
        return render(request, self.template_name, {'personal_loan_form': personal_loan_form})

    def form_valid(self, form):
        '''
        This method is called when valid form data has been posted.
        It should return an HttpResponse.
        '''
        loan_type = 'personal'
        existing_home_loans = Loan.objects.filter(user=self.request.user, loan_type=loan_type).exists()
        if existing_home_loans:
            # If an existing home loan is found, prevent the new loan application
            messages.error(self.request, "You've already taken a Personal Loan and are not eligible for another home loan.")
            return redirect('loans:apply_personal_loan')
        
        try:
            with transaction.atomic():
                form.instance.user = self.request.user
                form.save()  # Attempt to save the form instance
                messages.success(self.request, f"{loan_type.capitalize()} loan application submitted successfully!")
                return redirect(self.success_url)
        except IntegrityError:
            messages.error(self.request, f"An unexpected error occurred while processing your {loan_type} loan application.")
            return redirect(self.success_url)

    def form_invalid(self, form):
        ''' Adding an error message '''
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{error}")
                
        return render(self.request, self.template_name, {'personal_loan_form': form})
    
    def get_form_kwargs(self):
        """
        Pass additional kwargs to the form instance. Useful for passing the request object or other variables.
        """
        kwargs = super(PersonalLoanCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class LoanListView(ListView):
    model = Loan
    template_name = 'loans/loans_home.html'
    context_object_name = 'loans'  # context name to use in the template

    def get_queryset(self):
        """
        Override to return all loans (including specific types like HomeLoan and EducationLoan)
        for the currently logged-in user.
        """
        user = self.request.user
        loans = Loan.objects.filter(user=user).select_related('homeloan', 'educationloan')
        return loans


class PersonalLoanUpdateView(UpdateView):
    model = Loan
    form_class = LoanForm
    template_name = 'loans/loan_form.html'
    success_url = reverse_lazy('loan_list')  # Redirect to the loan list after update

    def form_valid(self, form):
        ''' Method is called when valid form data has been posted. '''
        response = super().form_valid(form)  # Saves the form instance
        return response


# =========================== Home Loan Views ===========================================
class HomeLoanCreateView(LoginRequiredMixin, FormView):
    template_name = 'loans/home_loan_form.html'
    form_class = HomeLoanForm
    success_url = reverse_lazy('loans:loan_home')  # Redirect to this URL after successful form submission

    def get(self, request):
        ''' 
        This method is called for GET requests
        '''
        if request.user.is_authenticated:
            home_loan_form = HomeLoanForm()
            return render(request, self.template_name, {'home_loan_form': home_loan_form})

    def form_valid(self, form):
        '''
            This method is called when valid form data has been POSTed.
        '''
        loan_type = 'home'
        existing_home_loans = Loan.objects.filter(user=self.request.user, loan_type=loan_type).exists()
        if existing_home_loans:
            # If an existing home loan is found, prevent the new loan application
            messages.error(self.request, "You've already taken a Home Loan and are not eligible for another home loan.")
            return redirect('loans:apply_home_loan')
        
        try:
            with transaction.atomic():
                form.instance.user = self.request.user
                form.save()  
                messages.success(self.request, f"{loan_type.capitalize()} loan application submitted successfully!")
                return HttpResponseRedirect(self.get_success_url())
        except IntegrityError:
            messages.error(self.request, f"An unexpected error occurred while processing your {loan_type} loan application.")
            return redirect('loans:apply_home_loan')
        
    def form_invalid(self, form):
        ''' Adding an error message for each form field that has an error '''
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{error}")
                
        return render(self.request, self.template_name, {'home_loan_form': form})

    def get_form_kwargs(self):
        """
        Pass additional kwargs to the form instance. Useful for passing the request object or other variables.
        """
        kwargs = super(HomeLoanCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


# =========================== Education Loan Views ========================================
class EducationLoanCreateView(LoginRequiredMixin, FormView):
    template_name = 'loans/education_loan_form.html'
    form_class = EducationLoanForm
    success_url = reverse_lazy('loans:loan_home')  # Ensure this is the correct URL for redirect after success

    def get(self, request):
        ''' Handles GET requests '''
        if request.user.is_authenticated:
            education_loan_form = EducationLoanForm(user=request.user)
            return render(request, self.template_name, {'form': education_loan_form})

    def form_valid(self, form):
        ''' Called when valid form data has been POSTed. Also redirect to success_url '''
        loan_type = 'education'
        existing_education_loans = Loan.objects.filter(user=self.request.user, loan_type=loan_type).exists()
        if existing_education_loans:
            # If an existing home loan is found, prevent the new loan application
            messages.error(self.request, "You've already taken a Home Loan and are not eligible for another home loan.")
            return redirect('loans:apply_education_loan')
        
        try:
            with transaction.atomic():
                form.instance.user = self.request.user
                form.save() 
                messages.success(self.request, f"{loan_type.capitalize()} loan application submitted successfully!")
                return HttpResponseRedirect(self.get_success_url())
        except IntegrityError:
            messages.error(self.request, f"An unexpected error occurred while processing your {loan_type} loan application.")
            return redirect('loans:apply_education_loan')  
        
    def form_invalid(self, form):
        ''' Adding an error message '''
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{error}")
                
        return render(self.request, self.template_name, {'education_loan_form': form})

    def get_form_kwargs(self):
        ''' Pass additional kwargs to the form instance. '''
        kwargs = super(EducationLoanCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


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
    
    
# ========================= University Post API View ========================================
@csrf_exempt
def add_university(request):
    if request.method == 'POST':
        
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        
        insurance = Insurance()
        
        insurance.number = body.get('number')
        insurance.company = body.get('company')
        insurance.premium = body.get('premium')
        
        insurance.save()
            
        return HttpResponse(insurance.id, insurance.number)
    
@csrf_exempt
def add_universities(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            if not isinstance(data, list):
                return HttpResponseBadRequest("Expected a list of data.")

            last_code = University.objects.all().aggregate(Max('code'))[
                            'code__max'] or 1000  # Start from 1000 to increment to 1001 next

            universities = []
            for uni_data in data:
                if 'institution' not in uni_data:
                    return HttpResponseBadRequest("Missing 'institution' in JSON data.")
                last_code += 1  # Increment code
                universities.append(University(name=uni_data['institution'], code=last_code))

            University.objects.bulk_create(universities)
            response_data = [{"name": uni.name, "code": uni.code} for uni in universities]
            return JsonResponse({"message": "Universities added successfully.", "universities": response_data},
                                status=201)

    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")
    except Exception as e:
        return HttpResponseBadRequest(f"Error saving universities: {str(e)}")
