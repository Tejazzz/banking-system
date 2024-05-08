import logging

from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.shortcuts import HttpResponseRedirect, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.db import connection
from django.views.generic import TemplateView, RedirectView, View, UpdateView, DeleteView

from .forms import UserRegistrationForm, UserAddressForm
from .models import CheckingBankAccount, SavingsBankAccount
from .models import CheckingBankAccount
from .forms import UserUpdateForm 

logger = logging.getLogger(__name__)
User = get_user_model()


class UserRegistrationView(TemplateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/user_registration.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(
                reverse_lazy('user_home')
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
                reverse_lazy('user_home')
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
    template_name = 'accounts/user_login.html'
    redirect_authenticated_user = False


class LogoutView(RedirectView):
    pattern_name = 'home'

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
        return super().get_redirect_url(*args, **kwargs)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'accounts/update_user.html'
    success_url = reverse_lazy('user_home')  # Redirect to the user profile or home page after update

    def get_object(self, queryset=None):
        return self.request.user  # Return the current user, do not fetch from URL

    def form_valid(self, form):
        messages.success(self.request, 'Your profile has been updated successfully.')
        return super().form_valid(form)

# ======================================== Checking Accounts Views ======================================
@method_decorator(login_required, name='dispatch')
class OpenAccountsView(TemplateView):
    template_name = 'accounts/open_accounts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # You can add more context variables if needed
        return context

def get_user_checking_account(user_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM accounts_checkingbankaccount
            WHERE id = %s AND account_type = 'CHECKING'
            LIMIT 1
        """, [user_id])
        row = cursor.fetchone()
    return row

class OpenCheckingAccountView(LoginRequiredMixin, View):
    template_name = 'accounts/open_checking_accounts.html'

    def get(self, request, *args, **kwargs):
        existing_account = CheckingBankAccount.objects.filter(user=request.user, account_type='CHECKING').first()
        # existing_account = get_user_checking_account(request.user.id)

        if existing_account:
            # If an account exists, inform the user and redirect
            messages.info(request, "You already have a checking account.")
            return redirect(reverse_lazy('accounts:accounts_home'))

        with transaction.atomic():
            # Create the checking account with default values
            account = CheckingBankAccount(
                user=request.user,
                date_opened=timezone.now(),
                balance=0.00,
                service_charge=10.00,
                account_type='CHECKING'
            )
            account.save()
            logger.info("Checking account successfully created for user %s", request.user)
            return redirect(reverse_lazy(
                'accounts:accounts_home'))  
    
class DeleteCheckingAccountView(LoginRequiredMixin, DeleteView):
    model = CheckingBankAccount
    template_name = 'accounts/delete_checking_account.html'
    success_url = reverse_lazy('accounts:accounts_home')

    def get_queryset(self):
       
        return self.model.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Checking account deleted successfully.")
        return super().delete(request, *args, **kwargs)


# ========================================== SAVINGS ACCOUNT ==========================================

class OpenSavingsAccountView(LoginRequiredMixin, View):
    template_name = 'accounts/open_savings_account.html'

    def get(self, request, *args, **kwargs):
        existing_account = SavingsBankAccount.objects.filter(user=request.user, account_type='SAVINGS').first()

        if existing_account:
            # If an account exists, inform the user and redirect
            messages.info(request, "You already have a savings account.")
            return redirect(reverse_lazy('accounts:accounts_home'))

        with transaction.atomic():
            # Create the savings account with default values
            account = SavingsBankAccount(
                user=request.user,
                date_opened=timezone.now(),
                balance=0.00,
                interest_rate=10.00,
                account_type='SAVINGS'
            )
            account.save()
            return redirect(reverse_lazy('accounts:accounts_home'))

class DeleteSavingsAccountView(LoginRequiredMixin, DeleteView):
    model = SavingsBankAccount
    template_name = 'accounts/delete_savings_account.html'
    success_url = reverse_lazy('accounts:accounts_home')  # Redirect here after deletion

    def get_queryset(self):
        """ Ensure that a user can only delete their own savings account. """
        return self.model.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Savings account deleted successfully.")
        return super().delete(request, *args, **kwargs)
    
# ============================= Account Details Home Page =============================================
class AccountDetailsView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/accounts_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Assuming you have different types of accounts under the same user
        context['accounts'] = self.request.user.account.all()
        return context
