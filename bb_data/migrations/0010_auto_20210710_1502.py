# Generated by Django 3.2.3 on 2021-07-10 19:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bb_data', '0009_auto_20210630_1225'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ColocationClientOwner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_account', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bb_data.colocationclient')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('owner_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bb_data.userprofile')),
            ],
        ),
        migrations.AddField(
            model_name='colocationclient',
            name='owners',
            field=models.ManyToManyField(related_name='client_owners', through='bb_data.ColocationClientOwner', to='bb_data.UserProfile'),
        ),
    ]
