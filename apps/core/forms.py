from django import forms
from django.core.validators import MinValueValidator
from .models import Schedule, TrainingHalls, TrainingType
from accounts.models import Trainer, CustomUser

class CreateGroupLessonForm(forms.ModelForm):
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