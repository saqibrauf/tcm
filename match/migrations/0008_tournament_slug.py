# Generated by Django 2.0.3 on 2018-05-14 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0007_auto_20180514_2312'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='slug',
            field=models.SlugField(default=''),
        ),
    ]
