# Generated by Django 2.0 on 2018-01-06 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_auto_20180106_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='group_name',
            field=models.CharField(default='Social Networking', max_length=50),
        ),
    ]
