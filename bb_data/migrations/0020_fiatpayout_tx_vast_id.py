# Generated by Django 3.2.3 on 2021-08-01 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bb_data', '0019_alter_cryptopayout_tx_hash'),
    ]

    operations = [
        migrations.AddField(
            model_name='fiatpayout',
            name='tx_vast_id',
            field=models.CharField(max_length=66, null=True, unique=True),
        ),
    ]