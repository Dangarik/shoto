from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from .forms import CreateGroupLessonForm
from .models import Schedule, TrainingHalls, TrainingType, Schedule, TrainingRegistration
from accounts.models import Trainer
from django.utils import timezone
import datetime
from django.contrib import messages

def all_section_view(request):
    sections = TrainingType.objects.all()
    return render(request, "all_section.html", {"sections": sections})

def detail_section_view(request, section_name):
    section = get_object_or_404(TrainingType, name=section_name)
    trainings = Schedule.objects.filter(section=section)
    context = {
        'section': section,
        'trainings': trainings,
    }
    return render(request, "detail_section.html", context)

def all_halls_view(request):
    halls = TrainingHalls.objects.all()
    return render(request, "halls/all_halls.html", {'halls': halls})

def hall_detail_view(request, hall_id):
    hall = get_object_or_404(TrainingHalls, pk=hall_id)
    trainings = Schedule.objects.filter(hall=hall)

    context = {
        'hall': hall,
        'trainings': trainings,
    }
    return render(request, "halls/hall_detail.html", context)

def all_trainers_view(request):
    trainers = Trainer.objects.all()

    context = {
        'trainers': trainers,
    }
    return render(request, "trainers/all_trainers.html", context)

def trainer_detail_view(request, trainer_id):
    trainer = get_object_or_404(Trainer, pk=trainer_id)
    trainings = Schedule.objects.filter(trainer=trainer)
    context = {
        'trainer': trainer,
        'trainings': trainings,
    }
    return render(request, "trainers/trainer_detail.html", context)

@login_required
def record_on_training(request, train_id):
    training = get_object_or_404(Schedule, id=train_id)

    user_has_recorded = Schedule.objects.filter(training=training, user=request.user).exists()

    if user_has_recorded:
        return JsonResponse({'recorded': True}, status=200)
    elif Schedule.status is not ['Started']:
        return redirect('training_detail', train_id=train_id)

    Schedule.objects.create(training=training, user=request.user)
    training.capacity += 1
    training.save()
    if Schedule.capacity >= Schedule.max_capacity:
        training.status = 'Заповнено'
        training.save()
    return redirect('training_detail', training_id=train_id)


@login_required
def record_on_training(request, train_id):
    training = get_object_or_404(Schedule, id=train_id)

    if training.status != 'Started':
        messages.error(request, 'Набір на це тренування закрито.')
        return redirect('training_detail', train_id=train_id)

    if training.capacity >= training.max_capacity:
        messages.error(request, 'На жаль, усі місця на це тренування вже зайняті.')
        if training.status != 'Full':
            training.status = 'Full'
            training.save()
        return redirect('training_detail', train_id=train_id)

    registration, created = TrainingRegistration.objects.get_or_create(
        user=request.user,
        schedule=training
    )

    if created:
        training.capacity += 1
        if training.capacity >= training.max_capacity:
            training.status = 'Full'
        training.save()
        messages.success(request, 'Ви успішно записалися на тренування!')
    else:
        messages.info(request, 'Ви вже записані на це тренування.')

    return redirect('training_detail', train_id=train_id)


@login_required
def cancel_training_record(request, train_id):
    training = get_object_or_404(Schedule, id=train_id)
    try:
        registration = TrainingRegistration.objects.get(user=request.user, schedule=training)
    except TrainingRegistration.DoesNotExist:
        messages.error(request, 'Ви не були записані на це тренування.')
        return redirect('training_detail', train_id=train_id)

    cancellation_deadline_hours = 1
    next_training_datetime = training.get_next_training_datetime()
    cancellation_deadline = next_training_datetime - datetime.timedelta(hours=cancellation_deadline_hours)

    if timezone.now() > cancellation_deadline:
        messages.error(request,
                       f'Скасувати запис можна було не пізніше, ніж за {cancellation_deadline_hours} години до початку тренування.')
        return redirect('training_detail', train_id=train_id)

    registration.delete()

    if training.capacity > 0:
        training.capacity -= 1

    if training.status == 'Full':
        training.status = 'Started'

    training.save()

    messages.success(request, 'Ваш запис на тренування було успішно скасовано.')
    return redirect('training_detail', train_id=train_id)


def training_detail(request, train_id):
    training = get_object_or_404(Schedule, id=train_id)
    now = timezone.now()
    training_type = get_object_or_404(TrainingType, name=training.training_type)

    next_training_start_dt = training.get_next_training_datetime()

    duration = datetime.datetime.combine(datetime.date.min, training.end_time) - datetime.datetime.combine(
        datetime.date.min, training.start_time)
    next_training_end_dt = next_training_start_dt + duration

    original_status = training.status
    if training.status in ['Started', 'Full']:
        if now >= next_training_start_dt and now < next_training_end_dt:
            training.status = 'Ongoing'
        elif now >= next_training_end_dt:
            training.status = 'Finished'

    if training.status != original_status:
        training.save()

    user_is_registered = False
    if request.user.is_authenticated:
        user_is_registered = TrainingRegistration.objects.filter(user=request.user, schedule=training).exists()

    context = {
        'training': training,
        'user_is_registered': user_is_registered,
        'training_type': training_type,
    }
    return render(request, "training_detail.html", context)

@login_required
def create_group_training(request):
    user = request.user
    if user.status == "main manager" or user.status == "manager":
        if request.method == "POST":
            form = CreateGroupLessonForm(request.POST)
            if form.is_valid():
                group_training = form.save(commit=False)
                group_training.author = request.user
                group_training.save()
                return redirect('training_detail', train_id=group_training.id)
            else:
                print(form.errors)
                return render(request, 'training_detail.html', {'form': form})
        else:
            form = CreateGroupLessonForm()
        return render(request, 'training_detail.html', {'form': form})




