# Generated by Django 3.2.12 on 2022-02-07 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bb_data', '0039_resourcerates'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resourcerates',
            name='resoruce',
        ),
        migrations.AddField(
            model_name='resourcerates',
            name='resource',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]