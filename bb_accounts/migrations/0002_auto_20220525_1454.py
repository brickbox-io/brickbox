# Generated by Django 3.2.12 on 2022-05-25 18:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bb_data', '0059_auto_20220511_1324'),
        ('bb_accounts', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserProfile',
        ),
        migrations.CreateModel(
            name='UserProfileProxy',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('bb_data.userprofile',),
        ),
    ]
