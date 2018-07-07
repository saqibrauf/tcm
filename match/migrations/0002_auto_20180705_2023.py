# Generated by Django 2.0.6 on 2018-07-05 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=50)),
                ('slug', models.SlugField(editable=False)),
            ],
        ),
        migrations.AddField(
            model_name='match',
            name='score_url',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
