# Generated by Django 3.2 on 2021-10-26 06:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0053_rename_service_dop_form_servicedopform'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ServiceDopForm',
            new_name='ServiceDop',
        ),
    ]