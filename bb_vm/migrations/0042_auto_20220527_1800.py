# Generated by Django 3.2.12 on 2022-05-27 22:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bb_vm', '0041_gpu_attached_to'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rentedgpu',
            options={'verbose_name_plural': 'D - Rented GPUs'},
        ),
        migrations.AlterField(
            model_name='rentedgpu',
            name='gpu',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='bb_vm.gpu', unique=True),
        ),
    ]
