from django.utils import timezone
from celery import shared_task

from accounts.models import BankAccount, SavingsBankAccount, CheckingBankAccount
from banking_system.celery import app
from transactions.models import Transaction


from django.db import transaction

import logging

logger = logging.getLogger(__name__)

@shared_task(name="update_account_balances")
def update_account_balances():
    logger.info("Running update_account_balances task")
    
    accounts = BankAccount.objects.filter(balance__gt=0)
    
    created_transactions = []
    updated_accounts = []

    for account in accounts:
        with transaction.atomic():
            if isinstance(account, SavingsBankAccount):
                interest = account.add_interest()
                transaction_obj = Transaction(
                    account=account,
                    transaction_type='Interest',
                    amount=interest
                )
                created_transactions.append(transaction_obj)
                logger.info(f"Added interest {interest} to SavingsAccount {account.id}")
                
            elif isinstance(account, CheckingBankAccount):
                # Deduct service charge for checking accounts
                service_charge = account.deduct_service_charge() 
                transaction_obj = Transaction(
                    account=account,
                    transaction_type='Charges',
                    amount=-service_charge 
                )
                created_transactions.append(transaction_obj)
                logger.info(f"Deducted charge {service_charge} from CheckingAccount {account.id}")
                
            updated_accounts.append(account)

    if created_transactions:
        Transaction.objects.bulk_create(created_transactions)

    if updated_accounts:
        BankAccount.objects.bulk_update(updated_accounts, ['balance'])



# @shared_task(name="update_account_balances")
# def update_account_balances():
#     accounts = BankAccount.objects.filter(balance__gt=0).select_related('user')

#     this_month = timezone.now().month

#     created_transactions = []
#     updated_accounts = []

#     for account in accounts:
#         if isinstance(account, SavingsBankAccount):
#             # Calculate and add interest for savings accounts
#             interest = account.add_interest() 
#             transaction_obj = Transaction(
#                 account=account,
#                 transaction_type='Interest',
#                 amount=interest
#             )
#             created_transactions.append(transaction_obj)
        
#         elif isinstance(account, CheckingBankAccount):
#             # Deduct service charge for checking accounts
#             service_charge = account.deduct_service_charge() 
#             transaction_obj = Transaction(
#                 account=account,
#                 transaction_type='Charges',
#                 amount=-service_charge 
#             )
#             created_transactions.append(transaction_obj)

#         updated_accounts.append(account)

#     if created_transactions:
#         Transaction.objects.bulk_create(created_transactions)

#     if updated_accounts:
#         BankAccount.objects.bulk_update(updated_accounts, ['balance'])
        

        
        
        
# @app.task(name="calculate_interest")
# def calculate_interest():
#     accounts = BankAccount.objects.filter(
#         balance__gt=0,
#         interest_start_date__gte=timezone.now(),
#         initial_deposit_date__isnull=False
#     ).select_related('account_type')

#     this_month = timezone.now().month

#     created_transactions = []
#     updated_accounts = []

#     for account in accounts:
#         if this_month in account.get_interest_calculation_months():
#             interest = account.account_type.calculate_interest(
#                 account.balance
#             )
#             account.balance += interest
#             account.save()

#             transaction_obj = Transaction(
#                 account=account,
#                 transaction_type=INTEREST,
#                 amount=interest
#             )
#             created_transactions.append(transaction_obj)
#             updated_accounts.append(account)

#     if created_transactions:
#         Transaction.objects.bulk_create(created_transactions)

#     if updated_accounts:
#         BankAccount.objects.bulk_update(
#             updated_accounts, ['balance']
#         )