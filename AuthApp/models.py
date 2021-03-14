from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models

# from AuthApp.managers import UserManager
from django.db.models.signals import pre_save
from django.dispatch import receiver


class BaseUser(AbstractUser):
    name = models.CharField(db_column='name', verbose_name='Name', blank=False, max_length=255, null=False)
    phoneNumber = models.CharField(db_column='phone_number', verbose_name='Phone Number', max_length=20, blank=True, null=True, default=None)
    otpVerified = models.BooleanField(db_column='otp_verified', verbose_name='OTP Verified', default=False)

    # objects = UserManager()

    class Meta(object):
        db_table = 'USERS'
        verbose_name = 'Users'
        verbose_name_plural = 'Users'
        unique_together = ('email',)

    def __str__(self):
        return self.email


@receiver(pre_save, sender=BaseUser)
def base_user_pre_save(sender, instance, *args, **kwargs):
    instance.username = instance.username or instance.email
    if not instance.password:
        instance.password = make_password(None)
    else:
        instance.password = make_password(instance.password)


class UserDeviceDetails(models.Model):
    user = models.ForeignKey(BaseUser, to_field='id', db_column='user_id', on_delete=models.CASCADE, related_name='user_device_details')
    platform = models.CharField(db_column='platform', max_length=25, blank=True, null=True, default=None)
    model = models.CharField(db_column='model', max_length=100, blank=True, null=True, default=None)
    osVersion = models.CharField(db_column='os_version', verbose_name='Os Version', max_length=100, blank=True, null=True, default=None)
    created = models.DateTimeField(db_column='created', auto_now=True)
    updated = models.DateTimeField(db_column='updated', auto_now_add=True)

    class Meta:
        db_table = 'USER_DEVICE_DETAILS'
        verbose_name = 'Users Device Details'
        verbose_name_plural = 'Users Device Details'
        ordering = ('created',)

    def __str__(self):
        return self.user.email


class UserDetails(models.Model):
    user = models.ForeignKey(BaseUser, to_field='id', db_column='user_id', on_delete=models.CASCADE, related_name='user_details')
    dob = models.CharField(db_column='date_of_birth', max_length=25, blank=True, null=True, default=None)
    gender = models.CharField(db_column='gender', max_length=25, blank=True, null=True, default=None)
    address = models.CharField(db_column='address', max_length=150, blank=True, null=True, default=None)
    city = models.CharField(db_column='city', max_length=50, blank=True, null=True, default=None)
    state = models.CharField(db_column='state', max_length=50, blank=True, null=True, default=None)
    country = models.CharField(db_column='country', max_length=50, blank=True, null=True, default=None)
    zip = models.CharField(db_column='zip', max_length=10, blank=True, null=True, default=None)
    created = models.DateTimeField(db_column='created', auto_now=True)
    updated = models.DateTimeField(db_column='updated', auto_now_add=True)

    class Meta:
        db_table = 'USER_DETAILS'
        verbose_name = 'Users Details'
        verbose_name_plural = 'Users Details'
        ordering = ('created',)

    def __str__(self):
        return self.user.email


EMAIL_TYPE_CHOICES = (
    ("Registration", "Registration"),
    ("Resend", "Resend"),
    ("ForgotPassword", "ForgotPassword")
)


class EmailDirectory(models.Model):
    user = models.ForeignKey(BaseUser, to_field='id', db_column='user_id', on_delete=models.CASCADE, related_name='user_rel_ced')
    created = models.DateTimeField(db_column='created', auto_now=True)
    isActive = models.BooleanField(db_column='is_active', default=True)
    type = models.CharField(db_column='email_type', max_length=25, blank=False, default=None, choices=EMAIL_TYPE_CHOICES)
    otpCode = models.CharField(db_column='otp_code', max_length=4, blank=False)

    class Meta:
        db_table = 'EMAIL_DIRECTORY'
        verbose_name = 'Customers Email Directory'
        verbose_name_plural = 'Customers Email Directory'

    def __str__(self):
        return self.user.email


class Categories(models.Model):
    catName = models.CharField(db_column='cat_name', verbose_name='English Name', max_length=1000, blank=False, null=False)
    catDescription = models.TextField(db_column='cat_description', verbose_name='English Description', max_length=5000, blank=False, null=False)
    telName = models.CharField(db_column='tel_name', verbose_name='Telugu Name', max_length=1000, blank=False, null=False)
    telPdfUrl = models.TextField(db_column='tel_pdf_url', verbose_name='Telugu Description', max_length=5000, blank=False, null=False)
    hindiName = models.CharField(db_column='hindi_name', verbose_name='Hindi Name', max_length=1000, blank=False, null=False)
    hindiPdfUrl = models.TextField(db_column='hindi_pdf_url', verbose_name='Hindi Description', max_length=5000, blank=False, null=False)
    isActive = models.BooleanField(db_column='is_active', verbose_name='Is Active', default=True)
    created = models.DateTimeField(db_column='created', auto_now=True)
    updated = models.DateTimeField(db_column='updated', auto_now_add=True)

    class Meta:
        db_table = 'CATEGORIES'
        verbose_name = 'Categories'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.catName


REQUEST_STATUS_CHOICES = (
    ("Open", "Open"),
    ("Pending", "Pending"),
    ("Completed", "Completed")
)

REQUEST_LOCATION_TYPE = (
    ("auto", "auto"),
    ("manual", "manual")
)


class ServiceRequest(models.Model):
    user = models.ForeignKey(BaseUser, to_field='id', db_column='user_id', on_delete=models.CASCADE, related_name='service_request')
    name = models.CharField(db_column='name', verbose_name='Name', blank=False, max_length=255, null=False)
    phoneNumber = models.CharField(db_column='phone_number', verbose_name='Phone Number', max_length=20, blank=True, null=True, default=None)
    email = models.CharField(db_column='email_id', verbose_name='Email Id', max_length=150, blank=False)
    message = models.TextField(db_column='message', verbose_name='Message', max_length=5000, blank=False, null=False)
    reply = models.TextField(db_column='reply', verbose_name='Reply', max_length=5000, blank=True, null=True)
    status = models.CharField(db_column='status', max_length=25, blank=False, choices=REQUEST_STATUS_CHOICES, default="Pending")
    locationType = models.CharField(db_column='location_type', verbose_name='Location Type', max_length=25, blank=False,
                                    choices=REQUEST_LOCATION_TYPE)
    address = models.CharField(db_column='address', max_length=150, blank=True, null=True, default=None)
    city = models.CharField(db_column='city', max_length=50, blank=True, null=True, default=None)
    state = models.CharField(db_column='state', max_length=50, blank=True, null=True, default=None)
    country = models.CharField(db_column='country', max_length=50, blank=True, null=True, default=None)
    zip = models.CharField(db_column='zip', max_length=10, blank=True, null=True, default=None)
    created = models.DateField(db_column='created', auto_now=True)
    updated = models.DateTimeField(db_column='updated', auto_now_add=True)

    class Meta:
        db_table = 'SERVICE_REQUEST'
        verbose_name = 'Service Request'
        verbose_name_plural = 'Service Requests'

    def __str__(self):
        return self.user.email