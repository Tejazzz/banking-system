from django.utils import timezone

from accounts.models import BankAccount
from banking_system.celery import app
from transactions.constants import INTEREST
from transactions.models import Transaction


@app.task(name="calculate_interest")
def calculate_interest():
    accounts = BankAccount.objects.filter(
        balance__gt=0,
        interest_start_date__gte=timezone.now(),
        initial_deposit_date__isnull=False
    ).select_related('account_type')

    this_month = timezone.now().month

    created_transactions = []
    updated_accounts = []

    for account in accounts:
        if this_month in account.get_interest_calculation_months():
            interest = account.account_type.calculate_interest(
                account.balance
            )
            account.balance += interest
            account.save()

            transaction_obj = Transaction(
                account=account,
                transaction_type=INTEREST,
                amount=interest
            )
            created_transactions.append(transaction_obj)
            updated_accounts.append(account)

    if created_transactions:
        Transaction.objects.bulk_create(created_transactions)

    if updated_accounts:
        BankAccount.objects.bulk_update(
            updated_accounts, ['balance']
        )
