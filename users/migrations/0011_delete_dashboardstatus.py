# Generated by Django 4.2.4 on 2023-10-12 02:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_dashboardstatus_route'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DashboardStatus',
        ),
    ]
