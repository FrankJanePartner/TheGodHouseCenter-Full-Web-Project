import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from rezonance.models import Video


class Command(BaseCommand):
    help = "Import rezonance video data from CSV"

    def handle(self, *args, **options):
        csv_file_path = os.path.join(
            settings.BASE_DIR, "mygeodata", "rezonance_video.csv"
        )
        if not os.path.exists(csv_file_path):
            self.stdout.write(self.style.ERROR("CSV file not found"))
            return

        with open(csv_file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                Video.objects.get_or_create(
                    id=int(row["id"]),
                    defaults={
                        "name": row["name"],
                        "slug": row["slug"],
                        "created_at": row["created_at"],
                        "images": row["images"],
                        "uploaded_at": row["uploaded_at"],
                        "audioFile": row["audioFile"],
                        "lyrics": row["lyrics"],
                    },
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Imported rezonance video: {row["name"]}')
                )
