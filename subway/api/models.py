from django.db import models

class Reading(models.Model):
    timestamp = models.DateTimeField()
    line = models.CharField(max_length=20, blank=False)
    status = models.CharField(max_length=40, blank=False)

    def __str__(self):
        return f'{self.line} {self.status} {self.timestamp}'

    class Meta:
        ordering = ('timestamp',)
