# Generated by Django 3.2.12 on 2022-05-27 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bb_vm', '0039_rename_gpu_count_virtualbrick_cpu_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='virtualbrick',
            name='memory_quantity',
            field=models.IntegerField(default=12),
        ),
    ]
