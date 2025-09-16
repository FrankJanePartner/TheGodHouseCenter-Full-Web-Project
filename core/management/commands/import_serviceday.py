import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import ServiceDay, Location, Category

class Command(BaseCommand):
    help = 'Import service day data from CSV'

    def handle(self, *args, **options):
        csv_file_path = os.path.join(settings.BASE_DIR, 'mygeodata', 'db', 'core_serviceday.csv')
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
                center_id = int(row['center_id'])
                location, created = Location.objects.get_or_create(
                    id=center_id,
                    defaults={
                        'name': f'Location {center_id}',
                        'category': category,
                        'address': '',
                        'description': '',
                        'thumbnail': '',
                        'directions': '',
                        'tel': '',
                        'email': ''
                    }
                )
                ServiceDay.objects.get_or_create(
                    center=location,
                    day=row['day'],
                    time=row['time']
                )
                self.stdout.write(self.style.SUCCESS(f'Imported service day for location {center_id}'))
