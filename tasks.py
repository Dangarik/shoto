import datetime
from django.utils import timezone
from apps.core.models import Schedule


def update_training_status():
    """
    Перевіряє та оновлює статуси тренувань ('Ongoing', 'Finished').
    """
    now = timezone.now()
    print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] Запуск завдання: update_training_status")

    trainings_to_check = Schedule.objects.exclude(status__in=['Finished', 'Ongoing'])

    if not trainings_to_check:
        print("Немає тренувань для перевірки.")
        return

    print(f"Знайдено {len(trainings_to_check)} тренувань для перевірки.")

    for training in trainings_to_check:
        next_start_dt = training.get_next_training_datetime()
        if not next_start_dt:
            continue

        duration = datetime.datetime.combine(datetime.date.min, training.end_time) - datetime.datetime.combine(
            datetime.date.min, training.start_time)
        next_end_dt = next_start_dt + duration

        original_status = training.status
        new_status = original_status

        if next_start_dt <= now < next_end_dt:
            new_status = 'Ongoing'
        elif now >= next_end_dt:
            new_status = 'Finished'

        if new_status != original_status:
            training.status = new_status
            training.save(update_fields=['status'])
            print(f"Оновлено статус тренування ID {training.id}: '{original_status}' -> '{new_status}'")

    print("Завдання update_training_status завершено.")