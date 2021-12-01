# Generated by Django 3.2.7 on 2021-12-01 02:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restoQuiz', '0008_auto_20211201_0318'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 1, 3, 22, 8, 976906)),
        ),
    ]
