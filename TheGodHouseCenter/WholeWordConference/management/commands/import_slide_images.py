import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from WholeWordConference.models import SlideImage, WholeWordConference


class Command(BaseCommand):
    help = "Import slide images data from CSV"

    def handle(self, *args, **options):
        csv_file_path = os.path.join(
            settings.BASE_DIR, "mygeodata", "WholeWordConference_slideimage.csv"
        )
        if not os.path.exists(csv_file_path):
            self.stdout.write(self.style.ERROR("CSV file not found"))
            return

        with open(csv_file_path, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                wwc = WholeWordConference.objects.get(id=row["wwc_id"])
                SlideImage.objects.get_or_create(
                    wwc=wwc, image=row["image"], created_at=row["created_at"]
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Imported slide image {row["image"]}')
                )
