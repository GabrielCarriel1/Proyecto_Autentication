# Generated by Django 4.1 on 2024-05-31 16:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_alter_product_supplier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.CharField(max_length=250, verbose_name='Nombre Categoría'),
        ),
        migrations.AlterField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(related_name='productos', to='core.category', verbose_name='Categoria'),
        ),
        migrations.AlterField(
            model_name='product',
            name='expiration_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 30, 16, 10, 37, 266517, tzinfo=datetime.timezone.utc), verbose_name='Fecha Caducidad'),
        ),
    ]
