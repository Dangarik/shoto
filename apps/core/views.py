from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from .forms import CreateTrainingForm, TrainingSearchForm
from .models import Schedule, TrainingHalls, TrainingType, Schedule, TrainingRegistration
from apps.accounts.models import Trainer, CustomUser
from django.utils import timezone
import datetime
from django.contrib import messages

@login_required
def create_training(request):
    user = request.user
    if user.status == "user":
        return render(request, 'home')

    if request.method == 'POST':
        form = CreateTrainingForm(request.POST)
        if form.is_valid():
            training = form.save(commit=False)
            training.author = request.user
            if user.status == 'trainer':
                training.trainer = user
                training_type_obj, _ = TrainingType.objects.get_or_create(name='Індивідуальні заняття')
                training.training_type = training_type_obj
            training.save()
            return redirect('core:training_detail', schedule_id=training.id)

    else:
        form = CreateTrainingForm()

    return render(request, 'create_training.html', {'form': form})



def detail_section_view(request, section_name):
    section = get_object_or_404(TrainingType, name=section_name)
    trainings = Schedule.objects.filter(section=section)
    context = {
        'section': section,
        'trainings': trainings,
    }
    return render(request, "detail_section.html", context)

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
def record_on_training(request, schedule_id):
    training = get_object_or_404(Schedule, id=schedule_id)
    user_has_signed = TrainingRegistration.objects.filter(schedule=training, user=request.user).exists()
    if user_has_signed:
        return JsonResponse({'recorded': True}, status=200)
    if not training.status == 'Started' or training.trainer == request.user:
        return redirect('core:training_detail', schedule_id=schedule_id)

    TrainingRegistration.objects.create(
        user=request.user,
        schedule=training
    )
    training.capacity += 1
    if training.capacity >= training.max_capacity:
        training.status = 'Full'
    training.save()
    return redirect('core:training_detail', schedule_id=schedule_id)


@login_required
def delate_training(request, schedule_id):
    training = get_object_or_404(Schedule, id=schedule_id)

    if request.user.id != training.trainer and not request.user.is_staff:
        return HttpResponseForbidden("Ви не маєте прав для видалення цієї петиції.")
    training.delete()
    return redirect('core:home')


@login_required
def cancel_training_record(request, schedule_id):
    training = get_object_or_404(Schedule, id=schedule_id)
    user_has_signed = TrainingRegistration.objects.filter(schedule=training, user=request.user).exists()

    if not user_has_signed:
        return JsonResponse({'unrecorded': True}, status=200)
    if training.status in ["Canceled","Finished","Ongoing"]:
        return redirect('core:training_detail', schedule_id=schedule_id)
    # логіка заборони скасування запису за годину
    cancellation_deadline_hours = 1
    next_training_datetime = training.get_next_training_datetime()
    cancellation_deadline = next_training_datetime - datetime.timedelta(hours=cancellation_deadline_hours)

    if timezone.now() > cancellation_deadline:
        messages.error(request,
                       f'Скасувати запис можна було не пізніше, ніж за {cancellation_deadline_hours} години до початку тренування.')
        return redirect('training_detail', schedule_id=schedule_id)

    TrainingRegistration.objects.filter(user=request.user,schedule=training).delete()
    training.capacity -= 1
    if training.status == "Full":
        if training.capacity < training.max_capacity:
            training.status = 'Started'
    training.save()
    return redirect('core:training_detail', schedule_id=schedule_id)



def training_detail(request, schedule_id):
    training = get_object_or_404(Schedule, id=schedule_id)
    training_type = get_object_or_404(TrainingType, name=training.training_type)
    trainer_info = get_object_or_404(Trainer, user=training.trainer)

    user_is_registered = False
    if request.user.is_authenticated:
        user_is_registered = TrainingRegistration.objects.filter(user=request.user, schedule=training).exists()

    context = {
        'training': training,
        'user_is_registered': user_is_registered,
        'training_type': training_type,
        'trainer_info': trainer_info,
    }
    return render(request, "training_detail.html", context)





def show_trainers_or_halls_or_sports(request, status=None):
    items = None
    title = "Інформація"

    if status:
        if status == "halls":
            items = TrainingHalls.objects.all()
            title = "Наші зали"
        elif status == "type":
            items = TrainingType.objects.all()
            title = "Види тренувань"
        elif status == "trainers":
            items = Trainer.objects.filter(user__status='trainer')
            title = "Тренери"
    else:
        return redirect("home")

    context = {
        'items': items,
        'title': title,
    }
    return render(request, 'list_by_type.html', context)


def training_list(request, status=None):
    form = TrainingSearchForm(request.GET or None)

    if status:
        schedules = Schedule.objects.all()
        if status == "group":
            schedules = Schedule.objects.exclude(training_type__name='Індивідуальні заняття')
    else:
        schedules = Schedule.objects.all()

    if form.is_valid():
        day_of_week = form.cleaned_data.get('day_of_week')
        if day_of_week:
            schedules = schedules.filter(day_of_week=day_of_week)

        training_type = form.cleaned_data.get('training_type')
        if training_type:
            schedules = schedules.filter(training_type=training_type)

        hall = form.cleaned_data.get('hall')
        if hall:
            schedules = schedules.filter(hall=hall)

        # Додано обробку тренера
        trainer = form.cleaned_data.get('trainer')
        if trainer:
            schedules = schedules.filter(trainer=trainer)

        sort_by = form.cleaned_data.get('sort_by')
        if sort_by:
            if sort_by in ['start_time', 'end_time', 'capacity']:
                schedules = schedules.order_by(sort_by)

    return render(request, 'training_list.html', {'form': form, 'schedules': schedules})


