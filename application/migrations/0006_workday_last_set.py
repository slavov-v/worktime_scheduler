# Generated by Django 2.0.5 on 2018-05-13 21:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0005_auto_20180513_1358'),
    ]

    operations = [
        migrations.AddField(
            model_name='workday',
            name='last_set',
            field=models.DateTimeField(default=datetime.datetime(1, 1, 1, 0, 0)),
        ),
    ]
