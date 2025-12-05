import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from ministrySchool.models import Attendee

class Command(BaseCommand):
    help = 'Import attendee data from CSV'

    def handle(self, *args, **options):
        csv_file_path = os.path.join(settings.BASE_DIR, 'mygeodata', 'db', 'ministrySchool_attendee.csv')
        if not os.path.exists(csv_file_path):
            self.stdout.write(self.style.ERROR('CSV file not found'))
            return

        with open(csv_file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Attendee.objects.get_or_create(
                    name=row['name'],
                    email=row['email'],
                    defaults={
                        'phone': row['phone'],
                        'how_will_you_attend': row['how_will_you_attend'],
                        'proof_of_payment': row['proof_of_payment']
                    }
                )
                self.stdout.write(self.style.SUCCESS(f'Imported attendee: {row["name"]}'))
