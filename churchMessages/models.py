from django.db import models
from core.models import Category, CommonInfo

# Create your models here.
class VideoMessage(CommonInfo):
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    images = models.ImageField(upload_to="media/videoMessages", height_field=None, width_field=None, max_length=None)
    year = models.DateField(null=True)
    video_id = models.CharField(max_length=300)

    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        verbose_name_plural = "VideoMessages"

class AudioMessage(CommonInfo):
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    images = models.ImageField(upload_to="media/AudioMessages", height_field=None, width_field=None, max_length=None)
    audio_id = models.CharField(max_length=300)
    year = models.DateField(null=True)
    
    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        verbose_name_plural = "AudioMessages"