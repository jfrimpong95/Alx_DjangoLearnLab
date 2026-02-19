from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Notification(models.Model):  # ✅ Notification(models.Model)
    recipient = models.ForeignKey(  # ✅ recipient
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    actor = models.ForeignKey(      # ✅ actor
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='actions'
    )
    verb = models.CharField(max_length=255)  # ✅ verb
    target_ct = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.CASCADE)
    target_id = models.PositiveIntegerField(blank=True, null=True)
    target = GenericForeignKey('target_ct', 'target_id')  # ✅ target
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)  # ✅ timestamp

    def __str__(self):
        return f"{self.actor.username} {self.verb} {self.recipient.username}"

