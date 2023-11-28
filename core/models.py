from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
# from datetime import datetime

# Create your models here.
class CommonInfo(models.Model):
    name = models.CharField(max_length=100)
    class_id = models.PositiveIntegerField()
    slug = models.SlugField(max_length=20)
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        # If the slug is not provided, create one from the name
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
        ordering = ["-name"]

class Category(CommonInfo):
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f'{self.name}'
    
    def get_absolute_url(self):
        return reverse('locationdetails:audioStream', args=[self.slug])
    
    class Meta:
        verbose_name_plural = "Categories"

class Location(CommonInfo):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    location_class = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return f'{self.name}'
    
    def get_absolute_url(self):
        return reverse('locationdetails:audioStream', args=[self.slug])
    
    class Meta:
        verbose_name_plural = "Locations"


class Leader(CommonInfo):
    images = models.ImageField(upload_to="media/leader", height_field=None, width_field=None, max_length=None)
    position = models.TextField()
    bio = models.TextField()

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('leaderdetails:audioStream', args=[self.slug])
    
    class Meta:
        verbose_name_plural = "Leaders"
