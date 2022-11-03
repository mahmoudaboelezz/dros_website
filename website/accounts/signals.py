from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from django.contrib.auth.models import Group
from onlinecourse.models import Learner
