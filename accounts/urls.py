from django.urls import path

from .views import UserRegistrationView, LogoutView, UserLoginView, OpenCheckingAccountView, OpenSavingsAccountView


app_name = 'accounts'

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="user_login"),
    path("logout/", LogoutView.as_view(), name="user_logout"),
    path("register/", UserRegistrationView.as_view(), name="user_registration"),
    
    path('open-checking-account/', OpenCheckingAccountView.as_view(), name='open_checking_account'),
    path('open-savings-account/', OpenSavingsAccountView.as_view(), name='open_savings_account'),
]
