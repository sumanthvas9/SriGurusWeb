# Generated by Django 3.1.7 on 2021-03-13 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AuthApp', '0016_auto_20210313_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicerequest',
            name='created',
            field=models.DateField(auto_now=True, db_column='created'),
        ),
    ]
