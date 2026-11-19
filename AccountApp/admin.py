from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Doctor, Patient, Specialty, User

admin.site.register(User, UserAdmin)


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Doctor)
class DoctorAdmin(UserAdmin):
    list_display = ('license_number', 'username', 'first_name', 'last_name', 'phone')
    fieldsets = UserAdmin.fieldsets + (
        ('Doctor information', {'fields': ('license_number', 'phone', 'specialties')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Doctor information', {'fields': ('license_number', 'phone', 'specialties')}),
    )
    filter_horizontal = ('groups', 'user_permissions', 'specialties')

    def get_readonly_fields(self, request, obj=None):
        readonly = super().get_readonly_fields(request, obj)
        return (*readonly, 'license_number') if obj else readonly


@admin.register(Patient)
class PatientAdmin(UserAdmin):
    list_display = ('national_id', 'username', 'first_name', 'last_name', 'phone', 'birth_date')
    fieldsets = UserAdmin.fieldsets + (
        ('Patient information', {'fields': ('national_id', 'phone', 'birth_date')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Patient information', {'fields': ('national_id', 'phone', 'birth_date')}),
    )

    def get_readonly_fields(self, request, obj=None):
        readonly = super().get_readonly_fields(request, obj)
        return (*readonly, 'national_id') if obj else readonly