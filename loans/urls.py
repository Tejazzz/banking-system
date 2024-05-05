from django.urls import path
from .views import HomeLoanFormView, EducationLoanFormView, EducationLoanWizard, PersonalLoanView
from loans import views

app_name = 'loans'

urlpatterns = [
    path('', views.loan_application, name='apply_loan'),
    path('save-insurance/', views.save_insurance),
    path('apply-personal-loan/', PersonalLoanView.as_view(), name='apply_personal-loan'),
    path('apply-education-loan/', EducationLoanWizard.as_view(), name='apply_education_loan'),
    path('apply-home-loan/', HomeLoanFormView.as_view(), name='apply_home_loan'),
    
    path('home-loan-success/', views.HomeLoanSuccessView.as_view(), name='home_loan_success'),
    
    path('home-loan/<uuid:id>/', HomeLoanFormView.as_view(), name='edit_home_loan'),  # UUID if your ID is a UUID
    path('education-loan/', EducationLoanFormView.as_view(), name='education_loan'),
    path('education-loan/<uuid:id>/', EducationLoanFormView.as_view(), name='edit_education_loan'),

]