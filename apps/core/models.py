from django.db import models
from django.conf import settings
import datetime
from django.utils import timezone

class TrainingHalls(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва залу")
    capacity = models.PositiveIntegerField(default=10, verbose_name="Місткість")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Зал"
        verbose_name_plural = "Зали"

class TrainingType(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Назва тренування")
    description = models.TextField(blank=True, null=True, verbose_name="Опис")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип тренування"
        verbose_name_plural = "Типи тренувань"

class Schedule(models.Model):
    day_choices = [
        (1, 'Понеділок'),
        (2, 'Вівторок'),
        (3, 'Середа'),
        (4, 'Четвер'),
        (5, 'П\'ятниця'),
        (6, 'Субота'),
        (7, 'Неділя'),
    ]

    hall = models.ForeignKey('TrainingHalls', on_delete=models.CASCADE, verbose_name="Зал")
    training_type = models.ForeignKey('TrainingType', on_delete=models.SET_NULL, null=True, blank=True,verbose_name="Тренування")
    max_capacity = models.PositiveIntegerField(default=1, verbose_name="Макс. місткість")
    capacity = models.PositiveIntegerField(default=0, verbose_name="Записано")
    day_of_week = models.IntegerField(choices=day_choices, verbose_name="День тижня")
    start_time = models.TimeField(verbose_name="Час початку")
    end_time = models.TimeField(verbose_name="Час закінчення")
    trainer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='trainer_schedule', verbose_name="Тренер")

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='training autor')

    status = models.CharField(
        max_length=10,
        choices=[
            ('Started', 'Набір'),
            ('Full', 'Заповнено'),
            ('Ongoing', 'Триває'),
            ('Finished', 'Закінчилося'),
        ],
        default='Started'
    )
    def __str__(self):
        training_name = self.training_type.name if self.training_type else "Вільно"
        return f"{self.get_day_of_week_display()} ({self.start_time:%H:%M}) в залі '{self.hall.name}': {training_name}"

    def get_next_training_datetime(self):
        today = timezone.now().date()
        days_ahead = self.day_of_week - today.isoweekday()
        if days_ahead < 0:
            days_ahead += 7
        training_date = today + datetime.timedelta(days=days_ahead)
        training_datetime = datetime.datetime.combine(training_date, self.start_time)
        # Робимо datetime об'єкт обізнаним про часову зону
        return timezone.make_aware(training_datetime, timezone.get_current_timezone())

    class Meta:
        verbose_name = "Запис у розкладі"
        verbose_name_plural = "Розклад"
        unique_together = ('hall', 'day_of_week', 'start_time')


class TrainingRegistration(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Користувач")
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='registrations',
                                 verbose_name="Тренування в розкладі")
    registration_time = models.DateTimeField(auto_now_add=True, verbose_name="Час запису")

    def __str__(self):
        return f"{self.user.username} записаний на {self.schedule}"

    class Meta:
        verbose_name = "Запис на тренування"
        verbose_name_plural = "Записи на тренування"
        unique_together = ('user', 'schedule')
