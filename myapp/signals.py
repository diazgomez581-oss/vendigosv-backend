from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile

User = get_user_model()

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if not created:
        return
    try:
        UserProfile.objects.get_or_create(user=instance)
    except Exception:
        # Evita romper el flujo de registro si algo falla
        pass
