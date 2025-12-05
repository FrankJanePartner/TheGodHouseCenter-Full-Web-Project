import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from contact.models import Testimony


class Command(BaseCommand):
    help = "Import testimony data from CSV"

    def handle(self, *args, **options):
        csv_file_path = os.path.join(
            settings.BASE_DIR, "mygeodata", "contact_testimony.csv"
        )
        if not os.path.exists(csv_file_path):
            self.stdout.write(self.style.ERROR("CSV file not found"))
            return

        with open(csv_file_path, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                Testimony.objects.get_or_create(
                    name=row["name"],
                    email=row["email"],
                    defaults={
                        "phone": row["phone"],
                        "location": row["location"],
                        "content": row["content"],
                        "image": row["image"],
                        "created_at": row["created_at"],
                    },
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Imported testimony: {row["name"]}')
                )
