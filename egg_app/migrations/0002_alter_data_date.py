# Generated by Django 5.1.4 on 2025-03-21 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('egg_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='date',
            field=models.DateField(),
        ),
    ]
