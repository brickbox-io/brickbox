# Generated by Django 3.2.7 on 2021-11-02 15:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bb_vm', '0021_alter_hostfoundation_serial_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hostfoundation',
            name='ssh_port',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='bb_vm.porttunnel'),
        ),
        migrations.AlterField(
            model_name='hostfoundation',
            name='sshtunnel_public_key',
            field=models.TextField(blank=True, null=True),
        ),
    ]
