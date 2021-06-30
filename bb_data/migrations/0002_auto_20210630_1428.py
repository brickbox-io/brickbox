# Generated by Django 3.2.3 on 2021-06-30 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bb_data', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cryptosnapshot',
            name='dollar_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='cryptosnapshot',
            name='balance',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='fiatsnapshot',
            name='balance',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
