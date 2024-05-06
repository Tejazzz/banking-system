from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, RedirectView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db import transaction

from .models import CheckingBankAccount, SavingsBankAccount
from .forms import UserRegistrationForm, UserAddressForm


User = get_user_model()


class UserRegistrationView(TemplateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/user_registration.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(
                reverse_lazy('transactions:transaction_report')
            )
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        registration_form = UserRegistrationForm(self.request.POST)
        address_form = UserAddressForm(self.request.POST)

        if registration_form.is_valid() and address_form.is_valid():
            user = registration_form.save()
            address = address_form.save(commit=False)
            address.user = user
            address.save()

            login(self.request, user)
            messages.success(
                self.request,
                (
                    # f'Thank You For Creating A Bank Account. '
                    # f'Your Account Number is {user.account.account_no}. '
                    'Thank You for registering with us!'
                )
            )
            return HttpResponseRedirect(
                reverse_lazy('transactions:deposit_money')
            )

        return self.render_to_response(
            self.get_context_data(
                registration_form=registration_form,
                address_form=address_form
            )
        )

    def get_context_data(self, **kwargs):
        if 'registration_form' not in kwargs:
            kwargs['registration_form'] = UserRegistrationForm()
        if 'address_form' not in kwargs:
            kwargs['address_form'] = UserAddressForm()

        return super().get_context_data(**kwargs)


class UserLoginView(LoginView):
    template_name='accounts/user_login.html'
    redirect_authenticated_user = False


class LogoutView(RedirectView):
    pattern_name = 'home'

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
        return super().get_redirect_url(*args, **kwargs)
    
    
    
# ======================================== Accounts Views ======================================
class OpenCheckingAccountView(LoginRequiredMixin, View):
    template_name = 'accounts/open_accounts.html'
    
    def get(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                # Create the checking account with default values
                account = CheckingBankAccount(
                    user=request.user,
                    date_opened=timezone.now(),
                    balance=0.00,
                    service_charge=10.00
                )
                account.save()  
                return HttpResponseRedirect(reverse_lazy('account_success'))  
        except Exception as e:
            messages.error(request, f'An error occurred while creating your checking account: {str(e)}')
            return HttpResponseRedirect(request.path)


class OpenSavingsAccountView(LoginRequiredMixin, View):
    template_name = 'accounts/open_accounts.html'
    def get(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                # Create the savings account with default values
                account = SavingsBankAccount(
                    user=request.user,
                    date_opened=timezone.now(),
                    balance=0.00,
                    interest_rate=10.00 
                )
                account.save()  
                return HttpResponseRedirect(reverse_lazy('account_success'))  
        except Exception as e:
            messages.error(request, f'An error occurred while creating your checking account: {str(e)}')
            return HttpResponseRedirect(request.path)

        