# Generated by Django 3.2.7 on 2021-10-05 17:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bb_vm', '0012_alter_vmlog_level'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vmlog',
            options={'verbose_name_plural': 'VM Logs'},
        ),
    ]