# Generated by Django 3.2.12 on 2022-05-11 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bb_data', '0057_userprofile_credit_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='billinghistory',
            name='destroy_vms_countdown_started',
            field=models.BooleanField(default=False),
        ),
    ]
