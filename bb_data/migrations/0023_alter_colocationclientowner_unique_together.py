# Generated by Django 3.2.3 on 2021-09-05 16:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bb_data', '0022_userprofile_brick_access'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='colocationclientowner',
            unique_together={('owner_profile', 'client_account')},
        ),
    ]
