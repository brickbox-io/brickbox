# Generated by Django 3.2.12 on 2022-03-03 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bb_data', '0051_alter_sshkey_pub_key'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentmethodowner',
            name='is_default',
        ),
        migrations.AddField(
            model_name='paymentmethod',
            name='is_default',
            field=models.BooleanField(default=False),
        ),
    ]
