# Generated by Django 3.2.12 on 2022-05-25 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bb_public', '0004_alter_contactus_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactus',
            name='is_closed',
            field=models.BooleanField(default=False),
        ),
    ]
