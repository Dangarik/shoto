from django import forms
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from .models import Schedule, TrainingHalls, TrainingType
from accounts.models import Trainer, CustomUser

User = get_user_model()
class CreateTrainingForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = [
            'day_of_week',
            'hall',
            'training_type',
            'max_capacity',
            'trainer',
            'start_time',
            'end_time',
        ]
        widgets = {
            'day_of_week': forms.Select(attrs={'class': 'form-control'}),
            'hall': forms.Select(attrs={'class': 'form-control'}),
            'training_type': forms.Select(attrs={'class': 'form-control'}),
            'trainer': forms.Select(attrs={'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'max_capacity': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class TrainingSearchForm(forms.Form):
    day_of_week = forms.ChoiceField(
        choices=[('', 'Будь-який')] + Schedule.day_choices,
        required=False,
        label='День тижня'
    )
    training_type = forms.ModelChoiceField(
        queryset=TrainingType.objects.all(),
        required=False,
        label='Тип тренування',
        empty_label='Будь-який'
    )
    hall = forms.ModelChoiceField(
        queryset=TrainingHalls.objects.all(),
        required=False,
        label='Зал',
        empty_label='Будь-який'
    )
    trainer = forms.ModelChoiceField(
        queryset=User.objects.filter(status='trainer'),
        required=False,
        label='Тренер',
        empty_label='Будь-який'
    )
    SORT_CHOICES = [
        ('', 'За замовчуванням'),
        ('start_time', 'Часом початку'),
        ('end_time', 'Часом закінчення'),
        ('capacity', 'Кількістю записаних'),
    ]
    sort_by = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        label='Сортувати за'
    )