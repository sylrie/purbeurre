# Generated by Django 3.0.3 on 2020-06-02 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0017_auto_20200320_1127'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseProductManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
