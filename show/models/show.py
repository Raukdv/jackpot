from django.db import models
from django.utils import timezone


class Show(models.Model):

    user = models.ForeignKey(
       'core.User', on_delete=models.CASCADE, related_name="show_user"
    )

    title = models.CharField(max_length=255, verbose_name=("Title"))

    content = models.TextField(verbose_name=("Content"), null=True, blank=True)

    date_creation = models.DateTimeField(default=timezone.now, verbose_name=("Date Creation"))

    class Meta:
        ordering = ['-date_creation']
        verbose_name = "Show"
        verbose_name_plural = "Shows"

    def __str__(self):
        return self.title