from django.db import models

class Enquire(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=25, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Enquiries'
        ordering = ['-created_at']

class PrayerRequest(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=25, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    should_contact = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'PrayerRequests'
        ordering = ['-created_at']