# Generated by Django 3.1.7 on 2021-03-13 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AuthApp', '0010_auto_20210313_1218'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='baseuser',
            options={'verbose_name': 'Users', 'verbose_name_plural': 'Users'},
        ),
        migrations.AlterModelOptions(
            name='categories',
            options={'verbose_name': 'Categories', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='emaildirectory',
            options={'verbose_name': 'Customers Email Directory', 'verbose_name_plural': 'Customers Email Directory'},
        ),
        migrations.AlterModelOptions(
            name='userdetails',
            options={'ordering': ('created',), 'verbose_name': 'Users Details', 'verbose_name_plural': 'Users Details'},
        ),
        migrations.AlterModelOptions(
            name='userdevicedetails',
            options={'ordering': ('created',), 'verbose_name': 'Users Device Details', 'verbose_name_plural': 'Users Device Details'},
        ),
        migrations.AlterField(
            model_name='baseuser',
            name='name',
            field=models.CharField(db_column='name', max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='baseuser',
            name='otpVerified',
            field=models.BooleanField(db_column='otp_verified', default=False, verbose_name='OTP Verified'),
        ),
        migrations.AlterField(
            model_name='baseuser',
            name='phoneNumber',
            field=models.CharField(blank=True, db_column='phone_number', default=None, max_length=20, null=True, verbose_name='Phone Number'),
        ),
        migrations.AlterField(
            model_name='categories',
            name='catDescription',
            field=models.TextField(db_column='cat_description', max_length=5000),
        ),
        migrations.AlterField(
            model_name='categories',
            name='hindiPdfUrl',
            field=models.TextField(db_column='hindi_pdf_url', max_length=5000),
        ),
        migrations.AlterField(
            model_name='categories',
            name='telPdfUrl',
            field=models.TextField(db_column='tel_pdf_url', max_length=5000),
        ),
        migrations.AlterField(
            model_name='userdevicedetails',
            name='osVersion',
            field=models.CharField(blank=True, db_column='os_version', default=None, max_length=100, null=True, verbose_name='Os Version'),
        ),
    ]
