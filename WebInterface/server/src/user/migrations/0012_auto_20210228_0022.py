# Generated by Django 3.1.7 on 2021-02-28 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_auto_20210228_0007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='twitteruser',
            name='profile_url',
            field=models.CharField(default='', max_length=200),
        ),
    ]
