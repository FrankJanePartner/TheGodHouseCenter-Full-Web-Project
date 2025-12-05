import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from events.models import Event
from core.models import Location


class Command(BaseCommand):
    help = "Import events data from CSV"

    def handle(self, *args, **options):
        csv_file_path = os.path.join(os.getcwd(), "mygeodata", "events_event.csv")
        self.stdout.write(self.style.SUCCESS(f"BASE_DIR: {settings.BASE_DIR}"))
        self.stdout.write(
            self.style.SUCCESS(f"Current working directory: {os.getcwd()}")
        )
        self.stdout.write(self.style.SUCCESS(f"Looking for CSV at: {csv_file_path}"))
        if not os.path.exists(csv_file_path):
            self.stdout.write(self.style.ERROR("CSV file not found"))
            return

        with open(csv_file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                location = Location.objects.get(id=row["location_id"])
                Event.objects.get_or_create(
                    name=row["name"],
                    slug=row["slug"],
                    created_at=row["created_at"],
                    active=row["active"].lower() == "true",
                    date=row["date"] if row["date"] else None,
                    description=row["description"],
                    location=location,
                    image=row["image"],
                    register_link=row["register_link"],
                    button_text=row["button_text"],
                )
                self.stdout.write(self.style.SUCCESS(f'Imported event {row["name"]}'))
