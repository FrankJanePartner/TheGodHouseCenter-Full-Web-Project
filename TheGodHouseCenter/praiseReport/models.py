from django.db import models
from core.models import CommonInfo
from tinymce.models import HTMLField
from django.urls import reverse

# Create your models here.
class Testimony(models.Model):
    Testifer_names = models.CharField(max_length=500)
    slug = models.SlugField(max_length=20)
    Testifer_center = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    Intro = models.CharField(max_length=360)
    content = HTMLField()
    
    def __str__(self):
        return f"{self.Testifer_names}'s testimony"
        
    def get_absolute_url(self):
        return reverse('testimony:details', args=[self.slug])
    
    class Meta:
        verbose_name_plural = "Testimonies"
        ordering = ['-created_at']

class TestimonyImage(models.Model):
    image = models.FileField(upload_to='bigTestImg')
    caption = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.caption}'

    class Meta:
        verbose_name_plural = "TestimonyImages"