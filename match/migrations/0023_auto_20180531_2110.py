# Generated by Django 2.0.3 on 2018-05-31 16:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0022_auto_20180529_0009'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-date']},
        ),
        migrations.AddField(
            model_name='series',
            name='date',
            field=models.DateField(default=datetime.datetime.today),
        ),
    ]
