# Generated by Django 5.1.7 on 2025-03-11 09:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_alter_carreview_car'),
    ]

    operations = [
        migrations.AddField(
            model_name='carreview',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='store.client'),
            preserve_default=False,
        ),
    ]
