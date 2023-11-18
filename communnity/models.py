from django.db import models
from core.models import CommonInfo

# Create your models here.
class Unit(CommonInfo):
    description = models.TextField()
    images = models.ImageField(upload_to='media/unit', height_field=None, width_field=None, max_length=None)

    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        verbose_name_plural = "Units"

class Church(CommonInfo):
    description = models.TextField()
    images = models.ImageField(upload_to='media/unit', height_field=None, width_field=None, max_length=None)

    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        verbose_name_plural = "Churches"