# Generated by Django 3.2.12 on 2022-02-12 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bb_vm', '0029_auto_20220120_2059'),
    ]

    operations = [
        migrations.AddField(
            model_name='gpu',
            name='is_enabled',
            field=models.BooleanField(default=True),
        ),
    ]
