from django.db import models

# Create your models here.

class DanceStyle(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='dance_styles/')

    def __str__(self):
        return self.name
