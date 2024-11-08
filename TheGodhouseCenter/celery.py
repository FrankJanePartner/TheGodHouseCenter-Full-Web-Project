from celery import Celery
from celery.schedules import crontab

app = Celery('TheGodHouseCenter')

app.conf.beat_schedule = {
    'publish-scheduled-posts-every-day-at-midnight': {
        'task': 'TheGodHouseCenter.tasks.publish_scheduled_posts',
        'schedule': crontab(minute=0, hour=0),  # Executes daily at midnight
    },
}

app.conf.timezone = 'UTC'


# myproject/celery.py
#from __future__ import absolute_import, unicode_literals
#import os
#from celery import Celery

# set the default Django settings module for the 'celery' program.
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

#app = Celery('myproject')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# namespace='CELERY' means all celery-related configuration keys
# should have a `CELERY_` prefix.
#app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
#app.autodiscover_tasks()

#@app.task(bind=True)
#def debug_task(self):
#    print(f'Request: {self.request!r}')

