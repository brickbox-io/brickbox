# Generated by Django 3.2.9 on 2021-12-05 20:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bb_data', '0027_colocationclient_term_agreement'),
        ('bb_vm', '0022_auto_20211102_1116'),
    ]

    operations = [
        migrations.CreateModel(
            name='EquipmentOwner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_account', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bb_data.colocationclient')),
                ('server', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bb_vm.hostfoundation')),
            ],
        ),
    ]
