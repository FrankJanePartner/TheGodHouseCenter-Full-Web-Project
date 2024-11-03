from django.db import models
from core.models import CommonInfo, Location

# Create your models here.
class Event(CommonInfo):
    active = models.BooleanField(default=False)
    date = models.DateTimeField()
    description = models.TextField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    image = models.FileField(upload_to='EventsImage')
    register_link = models.URLField(max_length=700, blank=True)
    button_text = models.CharField(max_length=700)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.active == True:
            self.active == "active"
        else:
            self.active == ""
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        ordering = ["-created_at"]
        
