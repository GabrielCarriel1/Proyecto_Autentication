# Generated by Django 5.0.6 on 2024-05-27 18:38

import proy_sales.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_alter_category_options_brand_logo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier',
            name='foto',
            field=models.ImageField(blank=True, default='suppliers/default.png', null=True, upload_to='suplier/'),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='address',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='ruc',
            field=models.CharField(max_length=13, validators=[proy_sales.utils.valida_cedula, proy_sales.utils.valida_ruc]),
        ),
    ]
