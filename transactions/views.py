from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import ListView

from accounts.models import BankAccount
from transactions.forms import DepositForm, WithdrawForm, DateRangeForm
from .models import Transaction


class DepositView(LoginRequiredMixin, View):
    template_name = 'transactions/deposit.html'
    form_class = DepositForm

    def get(self, request, account_no):
        account = get_object_or_404(BankAccount, pk=account_no)
        form = self.form_class(account=account)
        return render(request, self.template_name, {'form': form, 'account': account})

    def post(self, request, account_no):
        account = get_object_or_404(BankAccount, pk=account_no)
        form = self.form_class(request.POST, account=account)
        if form.is_valid():
            deposit_amount = form.cleaned_data['amount']
            new_balance = account.balance + deposit_amount
            transaction = Transaction(
                account=account,
                amount=deposit_amount,
                balance_after_transaction=new_balance,
                transaction_type="DEPOSIT"
            )
            transaction.save()
            account.balance = new_balance
            account.save()
            return redirect(reverse('accounts:accounts_home'))
        else:
            print("Form errors:", form.errors)  # Debug to see what errors are occurring
        return render(request, self.template_name, {'form': form, 'account': account})


class WithdrawView(LoginRequiredMixin, View):
    template_name = 'transactions/withdraw.html'
    form_class = WithdrawForm

    def get(self, request, account_no):
        account = get_object_or_404(BankAccount, pk=account_no)
        form = self.form_class(account=account)
        return render(request, self.template_name, {'form': form, 'account': account})

    def post(self, request, account_no):
        account = get_object_or_404(BankAccount, pk=account_no)
        form = self.form_class(request.POST, account=account)
        if form.is_valid():
            withdraw_amount = form.cleaned_data['amount']
            new_balance = account.balance - withdraw_amount
            transaction = Transaction(
                account=account,
                amount=withdraw_amount,
                balance_after_transaction=new_balance,
                transaction_type="WITHDRAW"
            )
            transaction.save()
            account.balance = new_balance
            account.save()
            return redirect(reverse('accounts:accounts_home'))
        else:
            print("Form errors:", form.errors)  # Debug to see what errors are occurring
        return render(request, self.template_name, {'form': form, 'account': account})


class TransactionListView(ListView):
    model = Transaction
    template_name = 'transactions/transaction_list.html'
    context_object_name = 'transactions'
    paginate_by = 5  # Adjust the number as needed

    def get_queryset(self):
        queryset = super().get_queryset()
        account_no = self.kwargs.get('account_no')  # Assumes 'account_number' is captured from URL

        # Filter by account number
        if account_no:
            account = get_object_or_404(BankAccount, account_no=account_no)
            queryset = queryset.filter(account=account)

        form = DateRangeForm(self.request.GET or None)
        if form.is_valid():
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')
            if start_date and end_date:
                queryset = queryset.filter(timestamp__date__range=(start_date, end_date))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date_form'] = DateRangeForm(self.request.GET or None)
        context['account_no'] = self.kwargs.get('account_no', None)
        return context
