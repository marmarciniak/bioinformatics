from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.



class DotPlot(models.Model):

    first_sequence = models.TextField(blank=True, null=True)
    second_sequence = models.TextField(blank=True, null=True)
    window = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    threshold = models.IntegerField(default=1, validators=[MinValueValidator(1)])
