from django.db import models

# Create your models here.
class Attendee(models.Model):

    name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    ministry = models.CharField(max_length=255, blank=True)
    godhouse_location = models.CharField(max_length=50, blank=True)
    local_church = models.TextField(blank=True)
    ministry_status = models.CharField(max_length=50, blank=True)
    how_did_you_know = models.CharField(max_length=50, blank=True)
    how_will_you_attend = models.CharField(max_length=50, blank=True)
    need_accommodation = models.CharField(max_length=3, blank=True)

    
    class Meta:
        verbose_name_plural = "Registrations"
    
    def __str__(self):
        return self.name
        
        

class FieldModel(models.Model):
    file = models.FileField(upload_to='wwc2024/')
    fileType = models.CharField(max_length=10)
    
    def __str__(self):
        return f"WWC2024 {self.fileType} {self.id}"