from django.db import models

# Create your models here.



class DotPlot(models.Model):

    first_sequence = models.TextField(blank=True, null=True)
    second_sequence = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=15, blank=True, null=True)
    window = models.IntegerField(default=1)
    minimal_precision = models.IntegerField(default=1)
