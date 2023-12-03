from django.db import models
from core.models import CommonInfo
from django.urls import reverse

# Create your models here.
class Unit(CommonInfo):
    description = models.TextField()
    images = models.ImageField(upload_to='media/unit')

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
            return reverse('community:unitsdetails', args=[self.slug])
    
    class Meta:
        verbose_name_plural = "Units"

class Church(CommonInfo):
    description = models.TextField()
    images = models.ImageField(upload_to='media/unit')

    def __str__(self):
        return f'{self.name}'
    
    def get_absolute_url(self):
        return reverse('community:churchesdetails', args=[self.slug])
    
    class Meta:
        verbose_name_plural = "Churches"