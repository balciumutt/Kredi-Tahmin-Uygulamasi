# Generated by Django 5.0.7 on 2024-07-26 16:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loan_prediction', '0008_alter_creditrisk_credit_score'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='creditrisk',
            name='current_credit_balance',
        ),
        migrations.RemoveField(
            model_name='creditrisk',
            name='maximum_open_credit',
        ),
        migrations.RemoveField(
            model_name='creditrisk',
            name='months_since_last_delinquent',
        ),
        migrations.RemoveField(
            model_name='creditrisk',
            name='number_of_open_accounts',
        ),
    ]
