# Generated by Django 3.2.3 on 2021-07-25 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bb_data', '0016_auto_20210720_1444'),
    ]

    operations = [
        migrations.AddField(
            model_name='cryptopayout',
            name='dated',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='fiatpayout',
            name='dated',
            field=models.DateTimeField(null=True),
        ),
    ]