# Generated by Django 4.2.4 on 2023-09-23 02:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='email',
        ),
    ]
