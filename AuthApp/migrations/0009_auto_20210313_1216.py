# Generated by Django 3.1.7 on 2021-03-13 06:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('AuthApp', '0008_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='categories',
            name='created',
            field=models.DateTimeField(auto_now=True, db_column='created'),
        ),
        migrations.AddField(
            model_name='categories',
            name='isActive',
            field=models.BooleanField(db_column='is_active', default=True),
        ),
        migrations.AddField(
            model_name='categories',
            name='updated',
            field=models.DateTimeField(auto_now_add=True, db_column='updated', default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
