# admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Patient

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields':
        ('first_name','email', 'last_name', 'birthdate', 'title', 'gender', 'mobileNumber', 'original_image_eyebrows','filtered_image_eyebrows',
        'original_image_mouth','filtered_image_mouth','original_image_eye','filtered_image_eye','previous_right_eyebrow_distance',
        'working_days','right_eyebrow_distance')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Patient)