from django.urls import path

from loans import views

app_name = 'loans'

urlpatterns = [
    path('', views.LoanListView.as_view(), name='loan_home'),
    path('apply-loan', views.loan_application, name='apply_loan'),

    path('apply-personal-loan/', views.PersonalLoanCreateView.as_view(), name='apply_personal_loan'),
    path('apply-home-loan/', views.HomeLoanCreateView.as_view(), name='apply_home_loan'),
    path('apply-education-loan/', views.EducationLoanCreateView.as_view(), name='apply_education_loan'),

    path('add-university/', views.add_universities, name='add_university'),
    path('save-insurance/', views.save_insurance)
]
