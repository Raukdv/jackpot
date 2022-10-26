#Model DJANGO LIBS
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
#Constants
from core.constants import ACTIVITY_TYPES

class Activity(models.Model):
    # Below the mandatory fields for generic relation
    content_type = models.ForeignKey(
        ContentType, 
        on_delete=models.CASCADE
    )

    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    user = models.ForeignKey(
       'core.User', 
       on_delete=models.CASCADE, 
       related_name="activity_user"
    )

    date_creation = models.DateTimeField(auto_now_add=True)

    activity_type = models.CharField(
        max_length=1, 
        choices=ACTIVITY_TYPES
    )
    
    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]
        ordering = ['-date_creation']
        verbose_name = "Activity"
        verbose_name_plural = "Activities"
