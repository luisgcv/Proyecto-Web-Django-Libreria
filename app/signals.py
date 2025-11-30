from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Rol

@receiver(post_migrate)
def crear_roles(sender, **kwargs):
    if sender.name == 'app':  # Cambia 'app' por el nombre real de tu aplicación
        Rol.objects.get_or_create(
            id=2,
            defaults={"rol": "user"}
        )
