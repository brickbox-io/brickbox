# Generated by Django 3.2.12 on 2022-02-07 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bb_data', '0035_billinghistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='billinghistory',
            name='status',
            field=models.CharField(choices=[('unpaid', 'Unpaid'), ('paid', 'Paid')], default='unpaid', max_length=32),
        ),
    ]
