# Generated by Django 2.0 on 2018-01-06 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_auto_20180106_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='group_name',
            field=models.CharField(default='Amazon window Shopping', max_length=50),
        ),
        migrations.AlterField(
            model_name='linklist',
            name='protocol',
            field=models.CharField(choices=[('HTTP://', 'HTTP'), ('HTTPS://', 'HTTPS')], default='HTTP://', max_length=10),
        ),
    ]
