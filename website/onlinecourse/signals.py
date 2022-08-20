from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Learner

@receiver(post_save, sender=User)
def post_save_create_learner(sender, instance, created, **kwargs):
    if created:
        Learner.objects.create(user=instance)
    learner = Learner.objects.create(user=instance)
    learner.save()