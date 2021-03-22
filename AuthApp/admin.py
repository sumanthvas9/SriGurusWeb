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
    list_per_page = 25

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'name', 'phoneNumber', 'otpVerified', 'registeredThrough')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # exclude = ('password',)
    #
    # readonly_fields = [
    #     'password',
    # ]

    def make_active(self, request, queryset):
        queryset.update(isActive=1)
        messages.success(request, "Selected record(s) marked as active successfully !!")

    def make_inactive(self, request, queryset):
        queryset.update(isActive=0)
        messages.success(request, "Selected record(s) marked as inactive successfully !!")

    actions = ['make_active', 'make_inactive']

    inlines = [UserDetailsInline]


# @admin.register(models.UserDeviceDetails)
# class UserDeviceDetailsAdmin(admin.ModelAdmin):
#     list_display = ('user', 'platform', 'model', 'osVersion')
#     search_fields = ("user__email__icontains", 'plateform__icontains', 'model__icontains', 'osVersion__icontains')


@admin.register(models.UserDetails)
class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ('user', 'dob', 'gender', 'city', 'country', 'zip')
    search_fields = ("user__email__icontains", 'dob__icontains', 'gender__icontains', 'city__icontains', 'country__icontains', 'zip__icontains')
    list_per_page = 25

    readonly_fields = [
        'user',
    ]


@admin.register(models.EmailDirectory)
class EmailDirectoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'otpCode', 'isActive')
    search_fields = ("user__email__icontains", 'type__icontains')
    list_per_page = 25

    readonly_fields = [
        'user',
    ]


@admin.register(models.Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('catName', 'catDescription', 'telName', 'telPdfUrl', 'hindiName', 'hindiPdfUrl', 'isActive')
    search_fields = (
        "catName__icontains", 'catDescription__icontains', 'telName__icontains', 'telPdfUrl__icontains', 'hindiName__icontains',
        'hindiPdfUrl__icontains')
    list_per_page = 25

    def make_active(self, request, queryset):
        queryset.update(isActive=1)
        messages.success(request, "Selected record(s) marked as active successfully !!")

    def make_inactive(self, request, queryset):
        queryset.update(isActive=0)
        messages.success(request, "Selected record(s) marked as inactive successfully !!")

    actions = ['make_active', 'make_inactive']


@admin.register(models.ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'email', 'phoneNumber', 'message', 'reply', 'status')
    search_fields = (
        "user__icontains", 'name__icontains', 'email__icontains', 'phoneNumber__icontains', 'message__icontains', 'reply__icontains',
        'status_icontains')
    list_per_page = 25

    readonly_fields = [
        'user',
    ]

    def has_add_permission(self, request):
        return False
