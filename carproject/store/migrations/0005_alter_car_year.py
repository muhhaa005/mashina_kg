# Generated by Django 5.1.7 on 2025-03-11 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_car_description_en_car_description_ru_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='year',
            field=models.PositiveSmallIntegerField(),
        ),
    ]
