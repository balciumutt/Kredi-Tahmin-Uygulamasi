from django import forms
from .models import CreditRisk
from django.contrib.auth.models import User

class CreditRiskForm(forms.ModelForm):
    class Meta:
        model = CreditRisk
        fields = [
            'current_loan_amount', 'term', 'credit_score', 
            'years_in_current_job', 'home_ownership', 'annual_income', 
            'monthly_debt', 'years_of_credit_history',
            'number_of_credit_problems',
            'bankruptcies', 'tax_liens', 'purpose'
        ]
        widgets = {
            'current_loan_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'term': forms.Select(attrs={'class': 'form-control'}),
            'credit_score': forms.NumberInput(attrs={'class': 'form-control'}),
            'years_in_current_job': forms.Select(attrs={'class': 'form-control'}),
            'home_ownership': forms.Select(attrs={'class': 'form-control'}),
            'annual_income': forms.NumberInput(attrs={'class': 'form-control'}),
            'monthly_debt': forms.NumberInput(attrs={'class': 'form-control'}),
            'years_of_credit_history': forms.NumberInput(attrs={'class': 'form-control'}),
            'months_since_last_delinquent': forms.NumberInput(attrs={'class': 'form-control'}),
            'number_of_open_accounts': forms.NumberInput(attrs={'class': 'form-control'}),
            'number_of_credit_problems': forms.NumberInput(attrs={'class': 'form-control'}),
            'current_credit_balance': forms.NumberInput(attrs={'class': 'form-control'}),
            'maximum_open_credit': forms.NumberInput(attrs={'class': 'form-control'}),
            'bankruptcies': forms.NumberInput(attrs={'class': 'form-control'}),
            'tax_liens': forms.NumberInput(attrs={'class': 'form-control'}),
            'purpose': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
    def clean_credit_score(self):
        credit_score = self.cleaned_data.get('credit_score')
        if credit_score < 300 or credit_score > 850:
            raise forms.ValidationError('Kredi skoru 300 ile 850 arasında olmalıdır.')
        return credit_score

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label='Parolayı Doğrula')

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Parolalar eşleşmiyor.')
        return cd['password2']