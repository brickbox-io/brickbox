# Generated by Django 3.2.12 on 2022-02-07 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bb_data', '0038_alter_billinghistory_invoice_link'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResourceRates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resoruce', models.CharField(blank=True, max_length=32, null=True)),
                ('stripe_price_id', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]