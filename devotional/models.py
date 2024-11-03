from django.db import models
from tinymce.models import HTMLField
from django.utils import timezone

# Create your models here.
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = HTMLField()
    publish_date = models.DateTimeField()
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def formatted_publish_date(self):
        return self.publish_date.strftime('%d-%B-%Y')