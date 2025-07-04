from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class Status(models.TextChoices):
    USER = 'user', _('Користувач')
    TRAINER = 'trainer', _('Тренер')
    MANAGER = 'manager', _('Менеджер')
    MAIN_MANAGER = 'main manager', _('Головний менеджер')

class Gender(models.TextChoices):
    MALE = 'MALE', _('Чоловік')
    FEMALE = 'FEMALE', _('Жінка')

class CustomUser(AbstractUser):
    email = models.EmailField(
        _('електронна пошта'),
        unique=True,
        help_text=_('Обов\'язкове поле. Використовується для входу в систему.')
    )

    full_name = models.CharField(_("ПІБ"), max_length=255, blank=True)
    date_of_birth = models.DateField(_("Дата народження"), null=True, blank=True)
    phone_number = models.CharField(_("Контактний телефон"), max_length=20, blank=True)
    gender = models.CharField(
        _("Стать"),
        max_length=10,
        choices=Gender.choices,
        blank=True
    )
    status = models.CharField(
        _("Статус/роль"),
        max_length=20,
        choices=Status.choices,
        default=Status.USER
    )

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _('Користувач')
        verbose_name_plural = _('Користувачі')

class Specialization(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Назва спеціалізації")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Спеціалізація')
        verbose_name_plural = _('Спеціалізації')

class Trainer(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='trainer_profile',
        verbose_name=_("Обліковий запис користувача")
    )
    photo = models.ImageField(upload_to='trainer_img/', blank=True, default='apps/core/static/img/avatar.png')
    specializations = models.ManyToManyField(
        Specialization,
        blank=True,
        verbose_name=_("Спеціалізації")
    )

    working_hours = models.CharField(
        max_length=255,
        verbose_name=_("Час роботи"),
        help_text=_("Наприклад: Пн-Пт, 09:00-19:00"),
        blank=True
    )

    def __str__(self):
        return f"Профіль тренера: {self.user.full_name or self.user.email}"

    class Meta:
        verbose_name = _('Профіль тренера')
        verbose_name_plural = _('Профілі тренерів')