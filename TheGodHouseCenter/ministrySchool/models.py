from django.db import models
from tinymce.models import HTMLField
from django.core.exceptions import ValidationError

# Create your models here.
class Attendee(models.Model):
    name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    how_will_you_attend = models.CharField(max_length=50, blank=True, null=True)
    proof_of_payment = models.FileField(upload_to="media/schoolOfMinistry")

    
    class Meta:
        verbose_name_plural = "Registrations"
    
    def __str__(self):
        return self.name
        
        

class FrontEndText(models.Model):
    text = HTMLField()
    def save(self, *args, **kwargs):
        # Check if there is already a record in the table
        if FrontEndText.objects.exists() and not self.pk:  
            raise ValidationError("Only one FrontEndText record is allowed.")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Front End Text"