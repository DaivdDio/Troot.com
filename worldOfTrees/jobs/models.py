from django.db import models

class Job(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='jobs/')
    description = models.TextField(blank=True, default='')
    sector = models.CharField(max_length=100, blank=True, default='')

    overview = models.TextField(blank=True, default='')

    study = models.JSONField(blank=True, null=True)
    responsibilities = models.JSONField(blank=True, null=True)
    where_they_work = models.JSONField(blank=True, null=True)
    skills_required = models.JSONField(blank=True, null=True)
    importance_of_work = models.JSONField(blank=True, null=True)
    how_troot_supports = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.title