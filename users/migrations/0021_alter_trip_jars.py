# Generated by Django 4.2.4 on 2023-12-20 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_alter_payments_amount_alter_sales_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='jars',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
