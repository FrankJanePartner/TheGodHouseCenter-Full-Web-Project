import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from praiseReport.models import Testimony


class Command(BaseCommand):
    help = "Import praise report testimonies from CSV"

    def handle(self, *args, **options):
        csv_file_path = os.path.join(
            settings.BASE_DIR, "mygeodata", "praiseReport_testimony.csv"
        )
        if not os.path.exists(csv_file_path):
            self.stdout.write(self.style.ERROR("CSV file not found"))
            return

        with open(csv_file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                Testimony.objects.get_or_create(
                    id=int(row["id"]),
                    defaults={
                        "Testifer_names": row["Testifer_names"],
                        "slug": row["slug"],
                        "Testifer_center": row["Testifer_center"],
                        "created_at": row["created_at"],
                        "Intro": row["Intro"],
                        "content": row["content"],
                    },
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Imported praise testimony: {row["Testifer_names"]}'
                    )
                )
