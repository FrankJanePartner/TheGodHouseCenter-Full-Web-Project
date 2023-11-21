from django.db import models
from core.models import CommonInfo

# Create your models here.
class Event(CommonInfo):
    status = models.TextField(blank=True)
    active = models.BooleanField(default=False)
    date = models.DateTimeField()
    duration = models.DurationField()
    description = models.TextField()
    location = models.TextField()
    image = models.ImageField(upload_to='EventsImage')
    register_link = models.URLField(max_length=700)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.active == True:
            self.status == "active"
        else:
            self.status == ""
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        ordering = ["name"]
        
