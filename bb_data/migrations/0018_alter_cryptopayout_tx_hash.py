# Generated by Django 3.2.3 on 2021-07-25 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bb_data', '0017_auto_20210725_1204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cryptopayout',
            name='tx_hash',
            field=models.CharField(max_length=66),
        ),
    ]
