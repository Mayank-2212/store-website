# Generated by Django 5.0.6 on 2024-07-05 11:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0002_category_products_slug_products_category_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='name',
            new_name='category_name',
        ),
        migrations.RenameField(
            model_name='productimage',
            old_name='image',
            new_name='product_image',
        ),
        migrations.RenameField(
            model_name='products',
            old_name='name',
            new_name='product_name',
        ),
    ]
