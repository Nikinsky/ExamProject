# Generated by Django 5.1.6 on 2025-02-08 07:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_feedback_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='model',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='car_model', to='store.model'),
            preserve_default=False,
        ),
    ]
