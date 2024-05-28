# Generated by Django 5.0.6 on 2024-05-27 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_product_cost_product_iva_alter_brand_state_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['description'], 'verbose_name': 'Categoría', 'verbose_name_plural': 'Categorías'},
        ),
        migrations.AddField(
            model_name='brand',
            name='logo',
            field=models.ImageField(blank=True, default='brands/default.png', null=True, upload_to='brands/'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='description',
            field=models.CharField(max_length=100, verbose_name='Descripción'),
        ),
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.CharField(max_length=100, verbose_name='Categoría'),
        ),
    ]