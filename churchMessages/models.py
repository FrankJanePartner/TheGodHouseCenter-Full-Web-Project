from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from core.models import Category

# Create your models here.
class CommonInfo(models.Model):
    name = models.CharField(max_length=100)
    class_id = models.PositiveIntegerField()
    slug = models.SlugField(max_length=20)
    created_at = models.DateTimeField(default=timezone.now)
    author = models.CharField(max_length=50, default='')

    def save(self, *args, **kwargs):
        # If the slug is not provided, create one from the name
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
        ordering = ["name"]

class VideoMessage(CommonInfo):
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    images = models.ImageField(upload_to="media/videoMessages", height_field=None, width_field=None, max_length=None)
    link = models.URLField()

    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        verbose_name_plural = "VideoMessages"

class AudioMessage(CommonInfo):
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    images = models.ImageField(upload_to="media/AudioMessages", height_field=None, width_field=None, max_length=None)
    file = models.FileField(upload_to='media/audios', max_length=100)
    
    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        verbose_name_plural = "AudioMessages"