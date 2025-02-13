# Generated by Django 5.1.6 on 2025-02-08 08:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_car_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='YearCar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.DateField()),
            ],
        ),
        migrations.AlterField(
            model_name='car',
            name='year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='car_year', to='store.yearcar'),
        ),
    ]
