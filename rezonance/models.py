from django.db import models
from django.urls import reverse
from tinymce.models import HTMLField
from core.models import Category, CommonInfo
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Album(CommonInfo):
    headerText = models.CharField(max_length=500, blank=True)
    link = models.CharField(max_length= 500, blank=True)
    images = models.FileField(upload_to="media/videoMessages")
    uploaded_at = models.DateTimeField(auto_now_add=True, blank=True)
    
    def __str__(self):
        return f'{self.name}'
        
    class Meta:
        verbose_name_plural = "Albums"
        ordering = ['-uploaded_at']
        
        
class SocailMedia(CommonInfo):
    link = models.CharField(max_length= 500, blank=True)
    image = models.FileField(upload_to="media/rezonanceMedia", blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True, blank=True)
    
    def __str__(self):
        return f'{self.name}'
        
    class Meta:
        verbose_name_plural = "SocailMedias"
        ordering = ['-uploaded_at']
        

class Video(CommonInfo):
    images = models.FileField(upload_to="media/videoMessages")
    audioFile = models.FileField(upload_to="media/Audio_File", blank=True)
    lyrics = HTMLField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f'{self.name}'
    
    def get_absolute_url(self):
        return reverse('rezonance:videoStream', args=[self.slug])

    class Meta:
        verbose_name_plural = "Videos"
        ordering = ['-uploaded_at']
        
      
class LifePerformance(CommonInfo):
    link = models.CharField(max_length= 500, blank=True)
    
    def __str__(self):
        return f'{self.name}'
        
    class Meta:
        verbose_name_plural = "LifePerformances"
        
        
class LifePerformanceImage(models.Model):
    lifePerformance = models.ForeignKey(LifePerformance, on_delete=models.CASCADE, related_name="product_image")
    image = models.FileField(
        verbose_name=_("image"),
        help_text=_("Upload a LifePerformance image"),
        upload_to="products/",
        default="images/default.png",
    )
    alt_text = models.CharField(
        verbose_name=_("Alternative text"),
        help_text=_("Please add alternative text"),
        max_length=255,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("LifePerformanceImage")
        verbose_name_plural = _("LifePerformanceImages")
