# Generated by Django 4.2 on 2024-05-14 19:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_product_expiration_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='expiration_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 13, 19, 57, 57, 318695, tzinfo=datetime.timezone.utc), verbose_name='Fecha Caducidad'),
        ),
    ]
