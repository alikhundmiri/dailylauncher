# Generated by Django 2.0 on 2017-12-24 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20171224_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='group_name',
            field=models.CharField(default='Apple News', max_length=50),
        ),
    ]
