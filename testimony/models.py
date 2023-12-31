from django.db import models
from core.models import CommonInfo
from django.urls import reverse

# Create your models here.
class Testimony(CommonInfo):
    Testifer_names = models.CharField(max_length=500)
    Testifer_images = models.ImageField(upload_to='testomy')
    Testifer_center = models.TextField()
    testimony_content = models.TextField()
    uploaded_at = models.DateField(auto_now=False, auto_now_add=False)
    
    def __str__(self):
        return f'{self.name}'
        
    def get_absolute_url(self):
        return reverse('details:audioStream', args=[self.slug])
    
    class Meta:
        ordering = ["-uploaded_at"]
        verbose_name_plural = "Testimonies"

class TestimonyImage(models.Model):
    image = models.ImageField(upload_to='bigTestImg')
    class_number = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name_plural = "TestimonyImages"