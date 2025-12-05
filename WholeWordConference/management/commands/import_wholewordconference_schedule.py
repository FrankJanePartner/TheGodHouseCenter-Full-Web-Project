import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from WholeWordConference.models import Schedule, WholeWordConference


class Command(BaseCommand):
    help = "Import Whole Word Conference schedule from CSV"

    def handle(self, *args, **options):
        csv_file_path = os.path.join(
            settings.BASE_DIR, "mygeodata", "WholeWordConference_schedule.csv"
        )
        if not os.path.exists(csv_file_path):
            self.stdout.write(self.style.ERROR("CSV file not found"))
            return

        with open(csv_file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                conference_id = int(row["wwc_id"])
                try:
                    conference = WholeWordConference.objects.get(id=conference_id)
                except WholeWordConference.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Conference with id {conference_id} not found"
                        )
                    )
                    continue

                Schedule.objects.get_or_create(
                    id=int(row["id"]),
                    defaults={
                        "wwc": conference,
                        "session": row["session"],
                        "time": row["time"],
                    },
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Imported schedule: {row["session"]}')
                )
