# Generated by Django 2.0 on 2018-01-03 06:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20171230_1714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='group_name',
            field=models.CharField(default='random Creeps of The Internet', max_length=50),
        ),
        migrations.AlterField(
            model_name='linklist',
            name='link',
            field=models.CharField(max_length=100, validators=[django.core.validators.URLValidator]),
        ),
    ]
