from django.db import models

class CreditRisk(models.Model):
    LOAN_STATUS_CHOICES = [
        ('Tamamen Ödendi', 'Tamamen Ödendi'),
        ('Tahsilat', 'Tahsilat'),
        ('Temerrüt', 'Temerrüt'),
        ('Güncel', 'Güncel'),
    ]
    
    TERM_CHOICES = [
        (0, 'Kısa Vade'),
        (1, 'Uzun Vade'),
    ]
    
    HOME_OWNERSHIP_CHOICES = [
        (0, 'Kira'),
        (1, 'Ev Sahibi'),
        (2, 'Ev Kredisi Ödüyor'),
        (3, 'Diğer'),
    ]

    APPLICATION_STATUS_CHOICES = [
        ('Beklemede', 'Beklemede'),
        ('Kabul Edildi', 'Kabul Edildi'),
        ('Reddedildi', 'Reddedildi'),
    ]
    
    user = models.ForeignKey('auth.User',blank=True,null=True ,on_delete=models.CASCADE, verbose_name='Kullanıcı')
    loan_status = models.CharField(max_length=20, choices=LOAN_STATUS_CHOICES, verbose_name='Kredi Durumu')
    current_loan_amount = models.PositiveIntegerField(verbose_name='İstenen Kredi Miktarı')
    term = models.IntegerField(choices=TERM_CHOICES, verbose_name='Vade')
    credit_score = models.FloatField(verbose_name='Kredi Skoru')
    
    YEARS_IN_CURRENT_JOB_CHOICES = [(str(i), str(i)) for i in range(11)]
    
    years_in_current_job = models.CharField(max_length=2, choices=YEARS_IN_CURRENT_JOB_CHOICES, verbose_name='Mevcut İşteki Yıl')
    home_ownership = models.IntegerField(choices=HOME_OWNERSHIP_CHOICES, verbose_name='Ev Sahipliği')
    annual_income = models.FloatField(verbose_name='Yıllık Gelir')
    monthly_debt = models.FloatField(verbose_name='Aylık Borç')
    years_of_credit_history = models.PositiveIntegerField(verbose_name='Kredi Geçmişi Yılı')
    number_of_credit_problems = models.PositiveIntegerField(verbose_name='Kredi Problemi Sayısı')
    bankruptcies = models.PositiveIntegerField(null=True, blank=True, verbose_name='İflaslar')
    tax_liens = models.PositiveIntegerField(null=True, blank=True, verbose_name='Vergi Hacizleri')
    purpose = models.CharField(max_length=255, verbose_name='Kredi Amacı')
    application_status = models.CharField(max_length=20, choices=APPLICATION_STATUS_CHOICES, default='Beklemede', verbose_name='Başvuru Durumu')

    def __str__(self):
        return f"Kredi Riski ID: {self.id}"
