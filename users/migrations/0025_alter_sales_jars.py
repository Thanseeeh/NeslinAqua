# Generated by Django 4.2.4 on 2024-02-22 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0024_creditdebitamounts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sales',
            name='jars',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=10),
        ),
    ]
