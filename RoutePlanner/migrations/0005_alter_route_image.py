# Generated by Django 3.2.3 on 2021-05-15 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RoutePlanner', '0004_auto_20210503_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='image',
            field=models.CharField(default='', max_length=8192),
        ),
    ]
