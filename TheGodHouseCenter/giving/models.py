from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from core.models import Category

# Create your models here.
class CommonInfo(models.Model):
    name = models.CharField(max_length=100)
    class_id = models.PositiveIntegerField()
    slug = models.SlugField(max_length=20)
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        # If the slug is not provided, create one from the name
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
        ordering = ["name"]

class Account(CommonInfo):
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        verbose_name_plural = "Accounts"