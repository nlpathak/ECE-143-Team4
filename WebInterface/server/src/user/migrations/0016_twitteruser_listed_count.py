# Generated by Django 3.1.7 on 2021-02-28 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0015_auto_20210228_0043'),
    ]

    operations = [
        migrations.AddField(
            model_name='twitteruser',
            name='listed_count',
            field=models.CharField(default='', max_length=200),
        ),
    ]