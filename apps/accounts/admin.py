from django.contrib import admin
from apps.accounts.models import CustomUser, Trainer, Specialization
from django.contrib.auth.admin import UserAdmin

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'full_name', 'status', 'is_staff')
    list_filter = ('status', 'gender', 'is_staff', 'is_superuser')
    search_fields = ('username', 'full_name', 'email')

    fieldsets = UserAdmin.fieldsets + (
        ('Додаткова інформація', {'fields': ('full_name', 'date_of_birth', 'phone_number', 'gender', 'status')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('full_name', 'email', 'gender', 'status')}),
    )

@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_specializations')
    search_fields = ('user__username', 'user__full_name', 'user__email')
    list_filter = ('specializations',)
    autocomplete_fields = ('user',)

    def get_specializations(self, obj):
        return ", ".join([s.name for s in obj.specializations.all()])

    get_specializations.short_description = 'Спеціалізації'

@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ('name', 'about')
    search_fields = ['name']



