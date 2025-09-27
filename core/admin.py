from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'experience_level', 'location', 'is_staff')
    list_filter = ('experience_level', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'location')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Información Adicional', {
            'fields': ('phone_number', 'location', 'experience_level', 'available_space')
        }),
    )