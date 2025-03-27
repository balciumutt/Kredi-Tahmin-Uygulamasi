# Generated by Django 5.0.7 on 2024-07-26 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan_prediction', '0006_alter_creditrisk_home_ownership_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creditrisk',
            name='annual_income',
            field=models.FloatField(verbose_name='Yıllık Gelir'),
        ),
        migrations.AlterField(
            model_name='creditrisk',
            name='maximum_open_credit',
            field=models.FloatField(verbose_name='Maksimum Açık Kredi'),
        ),
        migrations.AlterField(
            model_name='creditrisk',
            name='monthly_debt',
            field=models.FloatField(verbose_name='Aylık Borç'),
        ),
    ]
