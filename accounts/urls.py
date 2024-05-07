from django.urls import path

from accounts import views
from .views import UserRegistrationView, LogoutView, UserLoginView, OpenCheckingAccountView, OpenSavingsAccountView

app_name = 'accounts'

urlpatterns = [
    path("", views.AccountDetailsView.as_view(), name="accounts_home"),
    path("login/", UserLoginView.as_view(), name="user_login"),
    path("logout/", LogoutView.as_view(), name="user_logout"),
    path("register/", UserRegistrationView.as_view(), name="user_registration"),

    path('open-accounts/', views.OpenAccountsView.as_view(), name='open_accounts'),

    path('open-checking-account/', OpenCheckingAccountView.as_view(), name='open_checking_account'),
    path('open-savings-account/', OpenSavingsAccountView.as_view(), name='open_savings_account'),
]
