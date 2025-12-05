import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import Location, Category

class Command(BaseCommand):
    help = 'Import location data from CSV'

    def handle(self, *args, **options):
        csv_file_path = os.path.join(settings.BASE_DIR, 'mygeodata', 'core_location.csv')
        if not os.path.exists(csv_file_path):
            self.stdout.write(self.style.ERROR('CSV file not found'))
            return

        # Create categories if not exist
        categories = {
            2: {'name': 'Church', 'description': 'Physical church locations'},
            4: {'name': 'Online', 'description': 'Online church services'},
            5: {'name': 'Other', 'description': 'Other locations'}
        }
        for cat_id, data in categories.items():
            category, created = Category.objects.get_or_create(
                id=cat_id,
                defaults={
                    'name': data['name'],
                    'description': data['description']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {data["name"]}'))

        with open(csv_file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                category_id = int(row['category_id'])
                category = Category.objects.get(id=category_id)
                Location.objects.get_or_create(
                    id=int(row['id']),
                    defaults={
                        'name': row['name'],
                        'slug': row['slug'],
                        'created_at': row['created_at'],
                        'category': category,
                        'address': row['address'],
                        'description': row['description'],
                        'thumbnail': row['thumbnail'],
                        'directions': row['directions'],
                        'tel': row['tel'],
                        'email': row['email']
                    }
                )
                self.stdout.write(self.style.SUCCESS(f'Imported location: {row["name"]}'))
