
from django.contrib import admin
from django.urls import path, include
from .views import IndexView,user_login, user_logout, UserCreditRiskListView, UserRegisterView, AdminCreditRiskListView, PredictRiskView
from django.views.generic import TemplateView

urlpatterns = [
    path('',IndexView.as_view(), name='index'),
    path('success/', TemplateView.as_view(template_name='success.html'), name='success'),
    path('my-credit-risks/', UserCreditRiskListView.as_view(), name='my-credit-risks'),
    path('accounts/login/', user_login, name='login'),
    path('accounts/logout/', user_logout, name='logout'),
    path('accounts/register/', UserRegisterView.as_view(), name='register'),
    path('admin-credit-risks/', AdminCreditRiskListView.as_view(), name='admin-credit-risks'),
    path('predict-risk/', PredictRiskView.as_view(), name='predict-risk'),
]
