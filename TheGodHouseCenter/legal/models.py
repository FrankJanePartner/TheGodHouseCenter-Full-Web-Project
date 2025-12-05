from django.db import models
from django.urls import reverse
from tinymce.models import HTMLField

# Create your models here.
class Legal(models.Model):
    Privacy =  HTMLField()
    Terms =  HTMLField()
    
    def __str__(self):
        return f'Legal documents'