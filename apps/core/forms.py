from django import forms
from models import Schedule, TrainingHalls, TrainingType
from accounts.models import Trainer, CustomUser

class CreateGroupLessonForm(forms.ModelForm):
    day_of_week = forms.ChoiceField(
        choices=[('', 'Оберіть день')] + Schedule.day_choices,
        label="День проведення",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    hall = forms.ModelChoiceField(
        queryset=TrainingHalls.objects.all(),
        empty_label="Оберіть зал",
        label="Зал",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    training_type = forms.ModelChoiceField(
        queryset=TrainingType.objects.all(),
        empty_label="Оберіть тренування",
        label="Тип тренування",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    max_capacity = forms.PositiveIntegerField(label="Максимальна кількість", required=True)

    trainer = forms.ModelChoiceField(
        queryset=Trainer.objects.filter(trainer__isnull=False),
        empty_label="Оберіть тренера",
        label="Тренер",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    start_time = forms.TimeField(
        label="Час початку",
        required=True,
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'})
    )
    end_time = forms.TimeField(
        label="Час закінчення",
        required=True,
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'})
    )
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