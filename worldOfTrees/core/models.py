from django.db import models

# Create your models here.
# core/models.py


class SiteStats(models.Model):
    total_visits = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return f"Visits: {self.total_visits}"