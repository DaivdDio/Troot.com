from django.db import models

# Create your models here.
class BackupSchedule(models.Model):

    INTERVAL_CHOICES = [
        ("daily", "Daily"),
        ("weekly", "Weekly"),
        ("custom", "Custom"),
    ]

    DAYS = [
        ("mon", "Monday"),
        ("tue", "Tuesday"),
        ("wed", "Wednesday"),
        ("thu", "Thursday"),
        ("fri", "Friday"),
        ("sat", "Saturday"),
        ("sun", "Sunday"),
    ]

    enabled = models.BooleanField(default=False)
    interval = models.CharField(max_length=10, choices=INTERVAL_CHOICES, default="daily")

    days = models.CharField(max_length=50, blank=True)  # store "mon,tue,wed"
    time = models.TimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

class BackupLog(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)  # success / failed
    filename = models.CharField(max_length=255, blank=True)
    message = models.TextField(blank=True)