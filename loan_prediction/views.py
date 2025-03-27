from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import CreditRiskForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CreditRisk
from .forms import UserRegisterForm
from django.contrib.auth.models import Group
import joblib
from pathlib import Path
from sklearn.preprocessing import LabelEncoder
import os
import sklearn
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

class IndexView(LoginRequiredMixin,View):
    def get(self, request):
        form = CreditRiskForm()
        if request.user.groups.filter(name='Admin').exists():
            return redirect('admin-credit-risks')
        return render(request, 'index.html',{'form': form})
    
    def post(self, request):
        form = CreditRiskForm(request.POST)
        if form.is_valid():
            credit_risk = form.save(commit=False)
            credit_risk.user = request.user
            credit_risk.save()
            return redirect('success') 
        return render(request, 'index.html',{'form': form})
    

class PredictRiskView(View):
    def post(self, request):
        credit_risk_id = request.POST.get('credit_risk_id')
        credit_risk = get_object_or_404(CreditRisk, id=credit_risk_id)

        # Modeli yükleyin
        model = joblib.load(os.path.join(BASE_DIR, 'loan_prediction/RandomForest4.pkl'))

        data = {
            'Current Loan Amount': credit_risk.current_loan_amount,
            'Credit Score': credit_risk.credit_score,
            'Years in current job': float(credit_risk.years_in_current_job),
            'Home Ownership': credit_risk.home_ownership,
            'Annual Income': credit_risk.annual_income,
            'Monthly Debt': credit_risk.monthly_debt,
            'Years of Credit History': credit_risk.years_of_credit_history,
            'Number of Credit Problems': credit_risk.number_of_credit_problems,
            'Bankruptcies': credit_risk.bankruptcies,
            'Tax Liens': credit_risk.tax_liens,
            'Term_Short Term': credit_risk.term,
        }

        print(data)
        df = pd.DataFrame([data])

        # label_encoders = {}
        # for column in ['Term', 'Years in current job', 'Home Ownership']:
        #     le = LabelEncoder()
        #     df[column] = le.fit_transform(df[column])
        #     label_encoders[column] = le

        print(df)
        # Modelden tahmin alın
        prediction = model.predict(df)

        print(prediction)
        # Tahmin sonucunu kullanıcıya bildirin
        if prediction == 1:
            messages.success(request, f'{credit_risk.user.username} için kredi riski tahmini: Kabul Edildi')
        else:
            messages.error(request, f'{credit_risk.user.username} için kredi riski tahmini: Reddedildi')

        return redirect('admin-credit-risks')
    
class UserCreditRiskListView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        user_credit_risks = CreditRisk.objects.filter(user=request.user)
        return render(request, 'user_credit_risks.html', {'credit_risks': user_credit_risks})
    

class UserRegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            normal_user_group = Group.objects.get(name='Normal Kullanıcı')
            normal_user_group.user_set.add(user)
            login(request, user)
            return redirect('index')
        return render(request, 'register.html', {'form': form})
    

class AdminCreditRiskListView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        if request.user.groups.filter(name='Admin').exists():
            all_credit_risks = CreditRisk.objects.all()
            return render(request, 'admin_credit_risks.html', {'credit_risks': all_credit_risks})
        else:
            messages.error(request, 'Bu sayfaya erişim izniniz yok.')
            return redirect('index')

    def post(self, request):
        if request.user.groups.filter(name='Admin').exists():
            credit_risk_id = request.POST.get('credit_risk_id')
            action = request.POST.get('action')
            try:
                credit_risk = CreditRisk.objects.get(id=credit_risk_id)
                if action == 'approve':
                    credit_risk.application_status = 'Kabul Edildi'
                elif action == 'reject':
                    credit_risk.application_status = 'Reddedildi'
                credit_risk.save()
                messages.success(request, 'Başvuru durumu başarıyla güncellendi.')
            except CreditRisk.DoesNotExist:
                messages.error(request, 'Başvuru bulunamadı.')
            return redirect('admin-credit-risks')
        else:
            messages.error(request, 'Bu işlemi gerçekleştirme izniniz yok.')
            return redirect('index')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Geçersiz kullanıcı adı veya şifre')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

