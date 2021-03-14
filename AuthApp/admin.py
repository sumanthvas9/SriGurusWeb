from django.contrib import admin, messages

# Register your models here.
from AuthApp import models

admin.site.site_header = "SriGurus Admin"
admin.site.site_title = "SriGurus Admin Portal"
admin.site.index_title = "Welcome to SriGurus Admin Portal"


class UserDetailsInline(admin.StackedInline):
    model = models.UserDetails

    def get_extra(self, request, obj=None, **kwargs):
        return 1


@admin.register(models.BaseUser)
class BaseUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'phoneNumber', 'otpVerified', 'registeredThrough', 'is_active', 'is_superuser')
    search_fields = ("email__icontains", 'name__icontains', 'phoneNumber__icontains', 'registeredThrough__iexact')

    def make_active(self, request, queryset):
        queryset.update(is_active=1)
        messages.success(request, "Selected record(s) marked as active successfully !!")

    def make_inactive(self, request, queryset):
        queryset.update(is_active=0)
        messages.success(request, "Selected record(s) marked as inactive successfully !!")

    actions = ['make_active', 'make_inactive', 'filter_english', 'filter_telugu', 'filter_hindi']

    inlines = [UserDetailsInline]


@admin.register(models.UserDeviceDetails)
class UserDeviceDetailsAdmin(admin.ModelAdmin):
    list_display = ('user', 'platform', 'model', 'osVersion')
    search_fields = ("user__email__icontains", 'plateform__icontains', 'model__icontains', 'osVersion__icontains')


@admin.register(models.UserDetails)
class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ('user', 'dob', 'gender', 'city', 'country', 'zip')
    search_fields = ("user__email__icontains", 'dob__icontains', 'gender__icontains', 'city__icontains', 'country__icontains', 'zip__icontains')


@admin.register(models.EmailDirectory)
class EmailDirectoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'otpCode', 'isActive')
    search_fields = ("user__email__icontains", 'type__icontains')


@admin.register(models.Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('catName', 'catDescription', 'telName', 'telPdfUrl', 'hindiName', 'hindiPdfUrl', 'isActive')
    search_fields = (
        "catName__icontains", 'catDescription__icontains', 'telName__icontains', 'telPdfUrl__icontains', 'hindiName__icontains',
        'hindiPdfUrl__icontains')

    def make_active(self, request, queryset):
        queryset.update(is_active=1)
        messages.success(request, "Selected record(s) marked as active successfully !!")

    def make_inactive(self, request, queryset):
        queryset.update(is_active=0)
        messages.success(request, "Selected record(s) marked as inactive successfully !!")

    actions = ['make_active', 'make_inactive']


@admin.register(models.ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'email', 'phoneNumber', 'message', 'reply', 'status')
    search_fields = (
        "user__icontains", 'name__icontains', 'email__icontains', 'phoneNumber__icontains', 'message__icontains', 'reply__icontains',
        'status_icontains')
