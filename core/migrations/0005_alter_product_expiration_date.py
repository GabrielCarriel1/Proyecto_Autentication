# Generated by Django 5.0.6 on 2024-05-18 18:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_product_expiration_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='expiration_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 17, 18, 35, 1, 706578, tzinfo=datetime.timezone.utc), verbose_name='Fecha Caducidad'),
        ),
    ]
