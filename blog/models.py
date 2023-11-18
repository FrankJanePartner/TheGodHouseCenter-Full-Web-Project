from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.
class BlogCategories(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(default='')

    class Meta:
        verbose_name = ("BlogCategory")
        verbose_name_plural = "BlogCategories"

    def get_absolute_url(self):
        return reverse("blog:category_list", args=[self.slug])

    def __str__(self):
        return self.name


class Blog(models.Model):
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


class Subscriber(models.Model):
    user = models.EmailField(max_length=254)

    def __str__(self):
        return f"Subscriber: {self.id}"
