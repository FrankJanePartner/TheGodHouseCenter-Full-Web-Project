import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from events.models import Event
from core.models import Location, Category
from django.utils.dateparse import parse_datetime

class Command(BaseCommand):
    help = 'Import event data from CSV'

    def handle(self, *args, **options):
        csv_file_path = os.path.join(settings.BASE_DIR, 'mygeodata', 'db', 'events_event.csv')
        if not os.path.exists(csv_file_path):
            self.stdout.write(self.style.ERROR('CSV file not found'))
            return

        # Create default category if not exists
        category, created = Category.objects.get_or_create(
            name='Default',
            defaults={'description': 'Default category'}
        )

        with open(csv_file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                location_id = int(row['location_id'])
                location, created = Location.objects.get_or_create(
                    id=location_id,
                    defaults={
                        'name': f'Location {location_id}',
                        'category': category,
                        'address': '',
                        'description': '',
                        'thumbnail': '',
                        'directions': '',
                        'tel': '',
                        'email': ''
                    }
                )
                Event.objects.get_or_create(
                    name=row['name'],
                    slug=row['slug'],
                    defaults={
                        'active': row['active'] == '1',
                        'date': parse_datetime(row['date']),
                        'description': row['description'],
                        'location': location,
                        'image': row['image'],
                        'register_link': row['register_link'],
                        'button_text': row['button_text']
                    }
                )
                self.stdout.write(self.style.SUCCESS(f'Imported event: {row["name"]}'))
