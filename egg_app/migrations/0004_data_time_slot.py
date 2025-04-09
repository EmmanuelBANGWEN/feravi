# Generated by Django 5.1.4 on 2025-04-01 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('egg_app', '0003_data_chicken_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='data',
            name='time_slot',
            field=models.CharField(choices=[('08:00', '08:00'), ('13:00', '13:00'), ('17:00', '17:00')], default=0, max_length=5),
            preserve_default=False,
        ),
    ]
