# Generated by Django 4.2.4 on 2023-12-01 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_alter_sales_date_alter_store_created_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='status',
            field=models.CharField(default='Active', max_length=20),
        ),
    ]
