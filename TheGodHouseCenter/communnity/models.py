from django.db import models
from core.models import CommonInfo
from django.urls import reverse

# Create your models here.
class Unit(CommonInfo):
    description = models.TextField()
    images = models.FileField(upload_to='media/unit')

    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        verbose_name_plural = "Units"

class Church(CommonInfo):
    description = models.TextField()
    description2 = models.TextField()
    slogan = models.CharField(max_length=500)
    image = models.FileField(upload_to='media/Churches', null=True)
    Bible_verse = models.TextField()
    quote = models.TextField()

    def __str__(self):
        return f'{self.name}'
    
    def get_absolute_url(self):
        return reverse('community:churches', args=[self.slug])
    
    class Meta:
        verbose_name_plural = "Churches"