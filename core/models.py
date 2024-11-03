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
    address = models.TextField(null=True, blank=True)
    description = models.TextField(blank=True)
    thumbnail = models.FileField(upload_to='Locations_thumbmail')
    directions = models.URLField(blank=True)
    tel = models.CharField(blank=True, max_length=20)
    email = models.EmailField(max_length=255)

    def __str__(self):
        return f'{self.name}'
    
    def get_absolute_url(self):
        return reverse('core:locationdetails', args=[self.slug])
    
    class Meta:
        verbose_name_plural = "Locations"


class Leader(CommonInfo):
    images = models.FileField(upload_to="media/leader")
    position = models.TextField()
    bio = models.TextField()

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('core:leaderdetails', args=[self.slug])
    
    class Meta:
        verbose_name_plural = "Leaders"

        
class LeaderSocialMedia(models.Model):
    leader = models.ForeignKey(Leader, on_delete=models.CASCADE, related_name='leadersocialmedias')
    socialMediaName = models.CharField(max_length=255)
    link = models.URLField()
    
    def __str__(self):
        return f'{self.socialMediaName}'
        
    class Meta:
        verbose_name_plural = "LeaderSocialMedias"
        
    
class HeaderInfo(models.Model):
    display_text = models.CharField(max_length=255)
    link = models.URLField(blank=True)
    

    def __str__(self):
        return f'{self.display_text}'

    class Meta:
        verbose_name_plural = "HeaderInfos"


class ServiceDay(models.Model):
    center = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='service_days')
    day = models.CharField(max_length=255)
    time = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.center} - {self.day}'
        
    class Meta:
        verbose_name_plural = "ServiceDays"