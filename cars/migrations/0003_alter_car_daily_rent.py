# Generated by Django 5.0.8 on 2024-08-11 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='daily_rent',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
