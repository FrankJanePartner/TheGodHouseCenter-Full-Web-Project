from django.db import models
from core.models import Category, CommonInfo
from django.urls import reverse

# Create your models here.
class VideoMessage(CommonInfo):
    images = models.ImageField(upload_to="media/videoMessages", height_field=None, width_field=None, max_length=None)
    ItemNumber = models.IntegerField(default=0)
    seriesDescription =models.TextField()

    def __str__(self):
        return f'{self.name}'
    
    def get_absolute_url(self):
        return reverse('sermons:videoStream', args=[self.slug])

    class Meta:
        verbose_name_plural = "VideoMessages"

class AudioMessage(CommonInfo):
    images = models.ImageField(upload_to="media/AudioMessages", height_field=None, width_field=None, max_length=None)
    ItemNumber = models.IntegerField(default=0)
    seriesDescription =models.TextField()
    
    def __str__(self):
        return f'{self.name}'
    
    def get_absolute_url(self):
        return reverse('sermons:audioStream', args=[self.slug])
    
    def show_absolute_url(self):
        return reverse('sermons:sermondetail', args=[self.slug])
    
    class Meta:
        verbose_name_plural = "AudioMessages"


# class s