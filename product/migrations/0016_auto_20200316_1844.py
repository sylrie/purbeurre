# Generated by Django 3.0.3 on 2020-03-16 17:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0015_auto_20200316_1455'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='link',
        ),
        migrations.AlterField(
            model_name='favoriteproduct',
            name='saved_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Products'),
        ),
        migrations.DeleteModel(
            name='SavedProduct',
        ),
    ]
