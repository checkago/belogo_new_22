# Generated by Django 3.2 on 2021-12-07 08:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0062_auto_20211207_1136'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='images',
        ),
    ]
