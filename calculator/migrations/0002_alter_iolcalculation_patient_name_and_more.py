# Generated by Django 4.1.13 on 2024-07-03 12:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iolcalculation',
            name='patient_name',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='calculator.patient'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
    ]