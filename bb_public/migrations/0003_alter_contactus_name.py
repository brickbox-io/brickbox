# Generated by Django 3.2.12 on 2022-05-09 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bb_public', '0002_contactus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactus',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
