# Generated by Django 3.2.9 on 2021-12-05 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bb_data', '0026_userprofile_is_manager'),
    ]

    operations = [
        migrations.AddField(
            model_name='colocationclient',
            name='term_agreement',
            field=models.BooleanField(default=False),
        ),
    ]
