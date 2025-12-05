import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from WholeWordConference.models import WholeWordConference


class Command(BaseCommand):
    help = "Import Whole Word Conference data from CSV"

    def handle(self, *args, **options):
        csv_file_path = os.path.join(
            settings.BASE_DIR,
            "mygeodata",
            "WholeWordConference_wholewordconference.csv",
        )
        if not os.path.exists(csv_file_path):
            self.stdout.write(self.style.ERROR("CSV file not found"))
            return

        with open(csv_file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                WholeWordConference.objects.get_or_create(
                    id=int(row["id"]),
                    defaults={
                        "name": row["name"],
                        "date": row["date"],
                        "flyer": row["flyer"],
                        "slug": row["slug"],
                        "email_message": row["email_message"],
                        "end_date": row["end_date"],
                    },
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Imported Whole Word Conference: {row["name"]}')
                )
