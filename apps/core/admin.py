from django.contrib import admin
from apps.core.models import TrainingHalls, TrainingType, Schedule, TrainingRegistration

@admin.register(TrainingHalls)
class TrainingHallsAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity')
    search_fields = ('name',)


# Керування доступними типами тренувань
@admin.register(TrainingType)
class TrainingTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = (
        'get_day_of_week_display',
        'start_time',
        'hall',
        'training_type',
        'trainer',
        'capacity',
        'max_capacity',
        'status'
    )
    list_filter = ('day_of_week', 'status', 'hall', 'training_type', 'trainer', 'start_time')
    search_fields = ('hall__name', 'training_type__name', 'trainer__username', 'trainer__full_name')
    autocomplete_fields = ('hall', 'training_type', 'trainer', 'author')


@admin.register(TrainingRegistration)
class TrainingRegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'schedule', 'registration_time')
    list_filter = ('registration_time',)
    search_fields = ('user__username', 'user__full_name', 'schedule__training_type__name')
    autocomplete_fields = ('user', 'schedule')


from django.contrib import admin

# Register your models here.
