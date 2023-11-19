from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from core.models import Category, CommonInfo

# Create your models here.
class VideoMessage(CommonInfo):
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    images = models.ImageField(upload_to="media/videoMessages", height_field=None, width_field=None, max_length=None)
    link = models.URLField(max_length=500, blank=True, null=True)
    year = models.DateField(null=True)

    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        verbose_name_plural = "VideoMessages"

class AudioMessage(CommonInfo):
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    images = models.ImageField(upload_to="media/AudioMessages", height_field=None, width_field=None, max_length=None)
    link = models.URLField(max_length=500, blank=True, null=True)
    year = models.DateField(null=True)
    
    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        verbose_name_plural = "AudioMessages"