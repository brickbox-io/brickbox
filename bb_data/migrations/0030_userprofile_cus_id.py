# Generated by Django 3.2.9 on 2021-12-10 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bb_data', '0029_auto_20211207_1210'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='cus_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
