# Generated by Django 3.2.12 on 2022-06-13 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bb_data', '0059_auto_20220511_1324'),
    ]

    operations = [
        migrations.AddField(
            model_name='billinghistory',
            name='invoice_number',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]