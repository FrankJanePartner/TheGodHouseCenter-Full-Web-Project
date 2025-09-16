# myapp/tasks.py
from celery import shared_task
from django.utils import timezone
from myapp.models import Post

@shared_task
def publish_scheduled_posts():
    now = timezone.now()
    posts_to_publish = Post.objects.filter(publish_date__lte=now, is_published=False)
    for post in posts_to_publish:
        post.is_published = True
        post.save()
