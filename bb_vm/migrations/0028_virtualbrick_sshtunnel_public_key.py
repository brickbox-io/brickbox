# Generated by Django 3.2.10 on 2022-01-20 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bb_vm', '0027_alter_virtualbrickhistory_creator'),
    ]

    operations = [
        migrations.AddField(
            model_name='virtualbrick',
            name='sshtunnel_public_key',
            field=models.TextField(blank=True, null=True),
        ),
    ]
