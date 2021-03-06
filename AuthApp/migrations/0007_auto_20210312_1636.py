# Generated by Django 3.1.7 on 2021-03-12 11:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AuthApp', '0006_auto_20210312_1623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdevicedetails',
            name='user',
            field=models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, related_name='user_device_details', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dob', models.CharField(blank=True, db_column='date_of_birth', default=None, max_length=25, null=True)),
                ('gender', models.CharField(blank=True, db_column='gender', default=None, max_length=25, null=True)),
                ('address', models.CharField(blank=True, db_column='address', default=None, max_length=150, null=True)),
                ('city', models.CharField(blank=True, db_column='city', default=None, max_length=50, null=True)),
                ('state', models.CharField(blank=True, db_column='state', default=None, max_length=50, null=True)),
                ('country', models.CharField(blank=True, db_column='country', default=None, max_length=50, null=True)),
                ('zip', models.CharField(blank=True, db_column='zip', default=None, max_length=10, null=True)),
                ('created', models.DateTimeField(auto_now=True, db_column='created')),
                ('updated', models.DateTimeField(auto_now_add=True, db_column='updated')),
                ('user', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, related_name='user_details', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Users Details',
                'db_table': 'USER_DETAILS',
                'ordering': ('created',),
            },
        ),
    ]
