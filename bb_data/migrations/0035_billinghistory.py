# Generated by Django 3.2.12 on 2022-02-06 18:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bb_data', '0034_resourcetimetracking'),
    ]

    operations = [
        migrations.CreateModel(
            name='BillingHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('invoice_link', models.CharField(blank=True, max_length=100, null=True)),
                ('invoice_id', models.CharField(blank=True, max_length=100, null=True)),
                ('usage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bb_data.resourcetimetracking')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Billing History',
            },
        ),
    ]
