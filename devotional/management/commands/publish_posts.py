from django.core.management.base import BaseCommand
from django.utils import timezone
from devotional.models import Post

class Command(BaseCommand):
    help = 'Publish scheduled posts'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        posts_to_publish = Post.objects.filter(publish_date__lte=now, is_published=False)
        for post in posts_to_publish:
            post.is_published = True
            post.save()
            self.stdout.write(self.style.SUCCESS(f'Post "{post.title}" published'))
