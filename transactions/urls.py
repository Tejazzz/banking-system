from django.urls import path

from .views import DepositView, WithdrawView, TransactionListView

app_name = 'transactions'

urlpatterns = [
    path("deposit/<int:account_no>/", DepositView.as_view(), name="deposit_money"),
    path("withdraw/<int:account_no>/", WithdrawView.as_view(), name="withdraw_money"),
    path("list/<int:account_no>/", TransactionListView.as_view(), name="transaction_list")
]
