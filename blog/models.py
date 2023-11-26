from django.db import models
from django.utils import timezone
from django.urls import reverse
from core.models import CommonInfo #, Category

# Create your models here.
class Blog(CommonInfo):
    title = models.CharField(max_length=255)
    content = models.TextField()
    slug = models.SlugField(default='')
    images = models.ImageField(upload_to='blog_inages/', blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'Blogs'
        ordering = ('-created_at',)

    def get_absolute_url(self):
        return reverse("blog:blog_detail", args=[self.slug])
	
    def __str__(self):
        return self.title
