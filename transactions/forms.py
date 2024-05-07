from django import forms
from django.conf import settings
from django.utils.timezone import localdate

from .models import Transaction


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            'amount',
            'transaction_type'
        ]

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account', None)
        super().__init__(*args, **kwargs)
        self.fields['transaction_type'].disabled = True
        self.fields['transaction_type'].widget = forms.HiddenInput()


class DepositForm(TransactionForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the transaction type to "DEPOSIT" and make sure it's not editable or visible
        self.initial['transaction_type'] = "DEPOSIT"
        self.fields['transaction_type'].disabled = True
        self.fields['transaction_type'].widget = forms.HiddenInput()

    def clean_amount(self):
        min_deposit_amount = settings.MINIMUM_DEPOSIT_AMOUNT
        amount = self.cleaned_data.get('amount')
        if amount < min_deposit_amount:
            raise forms.ValidationError(
                f'You need to deposit at least {min_deposit_amount} $'
            )
        return amount


class WithdrawForm(TransactionForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the transaction type to "WITHDRAW" and make sure it's not editable or visible
        self.initial['transaction_type'] = "WITHDRAWAL"
        self.fields['transaction_type'].disabled = True
        self.fields['transaction_type'].widget = forms.HiddenInput()

    def clean_amount(self):
        account = self.account

        balance = account.balance

        amount = self.cleaned_data.get('amount')

        if amount > balance:
            raise forms.ValidationError(
                f'You have {balance} $ in your account. '
                'You can not withdraw more than your account balance'
            )

        return amount


class DateRangeForm(forms.Form):
    start_date = forms.DateField(label='Start Date', widget=forms.DateInput(attrs={'type': 'date'}), initial=localdate)
    end_date = forms.DateField(label='End Date', widget=forms.DateInput(attrs={'type': 'date'}), initial=localdate)

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if start_date > end_date:
                raise forms.ValidationError("End date should be greater than start date.")
        return cleaned_data
