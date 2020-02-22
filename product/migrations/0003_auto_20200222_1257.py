# Generated by Django 3.0.3 on 2020-02-22 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20200221_1916'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='ingredients',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='nutriments',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='nutriscore',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='details',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='img',
            field=models.URLField(max_length=300),
        ),
        migrations.AlterField(
            model_name='product',
            name='link',
            field=models.URLField(max_length=300),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='product',
            name='stores',
            field=models.TextField(),
        ),
    ]
