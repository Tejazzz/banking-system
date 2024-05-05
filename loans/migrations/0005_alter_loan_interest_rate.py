# Generated by Django 5.0.4 on 2024-05-04 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0004_alter_insurance_company_alter_loan_interest_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='interest_rate',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=5),
        ),
    ]
