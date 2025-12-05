import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from sermons.models import AudioMessage

class Command(BaseCommand):
    help = 'Import audio messages data from CSV'

    def handle(self, *args, **options):
        csv_file_path = os.path.join(settings.BASE_DIR, 'mygeodata', 'sermons_audiomessage_rows.csv')
        if not os.path.exists(csv_file_path):
            self.stdout.write(self.style.ERROR('CSV file not found'))
            return

        with open(csv_file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                AudioMessage.objects.get_or_create(
                    name=row['name'],
                    slug=row['slug'],
                    created_at=row['created_at'],
                    link=row['link'],
                    images=row['images'],
                    seriesDescription=row['seriesDescription'],
                    uploaded_at=row['uploaded_at']
                )
                self.stdout.write(self.style.SUCCESS(f'Imported audio message {row["name"]}'))
