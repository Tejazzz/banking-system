from django.urls import path
from loans import views

app_name = 'loans'

urlpatterns = [
    path('', views.loan_application, name='apply_loan'),
    # path('loans/', views.LoanListView.as_view(), name='loan_list'),
    path('save-insurance/', views.save_insurance),
    path('apply-personal-loan/', views.PersonalLoanCreateView.as_view(), name='apply_personal-loan'),
    path('apply-home-loan/', views.HomeLoanCreateView.as_view(), name='apply_home_loan'),
    path('apply-education-loan/', views.EducationLoanWizard.as_view(), name='apply_education_loan'),
    
    path('home-loan-success/', views.HomeLoanSuccessView.as_view(), name='home_loan_success'),
    
    path('loans-list/', views.LoanListView.as_view(), name='loans_list'),
    
    # path('home-loan/<uuid:id>/update', views.HomeLoanCreateView.as_view(), name='edit_home_loan'),  # UUID if your ID is a UUID
    # path('education-loan/', views.EducationLoanFormView.as_view(), name='education_loan'),
    # path('education-loan/<uuid:id>/', views.EducationLoanFormView.as_view(), name='edit_education_loan'),

]