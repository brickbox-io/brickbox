# Generated by Django 3.2.12 on 2022-02-20 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bb_vm', '0030_gpu_is_enabled'),
    ]

    operations = [
        migrations.AddField(
            model_name='virtualbrick',
            name='is_booting',
            field=models.BooleanField(default=True),
        ),
    ]
