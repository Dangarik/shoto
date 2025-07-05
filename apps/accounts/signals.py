from django.db.models.signals import post_save, post_delete, pre_init
from django.dispatch import receiver
from apps.accounts.models import Trainer
@receiver(post_save, sender=Trainer)
def create_or_update_user_role(sender, instance, created, **kwargs):
    """
    Ця функція викликається щоразу після збереження об'єкта Trainer.
    """
    if created:
        user = instance.user
        new_status = "trainer"
        if user.status != new_status:
            user.status = new_status
            user.save(update_fields=['status'])


@receiver(post_delete, sender=Trainer)
def remove_user_role(sender, instance, **kwargs):
    """
    Коли профіль тренера видаляється, змінюємо роль користувача назад на 'Клієнт'.
    """
    print(sender)
    user = instance.user
    new_status = "user"
    if user.status != new_status:
        user.status = new_status
        user.save(update_fields=['status'])