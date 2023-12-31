from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
# from datetime import datetime

# Create your models here.
class CommonInfo(models.Model):
    name = models.CharField(max_length=100)
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
        return reverse('core:category_list', args=[self.slug])
    
    class Meta:
        verbose_name_plural = "Categories"

class Location(CommonInfo):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    address = models.TextField()
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to='Locations_thumbmail')
    image = models.ImageField(upload_to='Locations_images')
    tel = models.CharField(blank=True, max_length=20)
    email = models.EmailField(max_length=255)

    def __str__(self):
        return f'{self.name}'
    
    def get_absolute_url(self):
        return reverse('core:locationdetails', args=[self.slug])
    
    class Meta:
        verbose_name_plural = "Locations"


class Leader(CommonInfo):
    images = models.ImageField(upload_to="media/leader", height_field=None, width_field=None, max_length=None)
    position = models.TextField()
    bio = models.TextField()

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('core:leaderdetails', args=[self.slug])
    
    class Meta:
        verbose_name_plural = "Leaders"


class ServiceDay(models.Model):
    center = models.ForeignKey(Location, on_delete=models.CASCADE)
    day = models.CharField(max_length=255)
    time = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'
    class Meta:
        verbose_name_plural = "ServiceDays"