import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from WholeWordConference.models import Attendee, WholeWordConference


class Command(BaseCommand):
    help = "Import Whole Word Conference attendees from CSV"

    def handle(self, *args, **options):
        csv_file_path = os.path.join(
            settings.BASE_DIR, "mygeodata", "WholeWordConference_attendee.csv"
        )
        if not os.path.exists(csv_file_path):
            self.stdout.write(self.style.ERROR("CSV file not found"))
            return

        with open(csv_file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                conference_id = int(row["whole_word_conference_id"])
                try:
                    conference = WholeWordConference.objects.get(id=conference_id)
                except WholeWordConference.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Conference with id {conference_id} not found"
                        )
                    )
                    continue

                Attendee.objects.get_or_create(
                    id=int(row["id"]),
                    defaults={
                        "whole_word_conference": conference,
                        "first_name": row["first_name"],
                        "last_name": row["last_name"],
                        "phone": row["phone"],
                        "ministry": row["ministry"],
                        "ministry_status": row["ministry_status"],
                        "how_did_you_know": row["how_did_you_know"],
                        "how_will_you_attend": row["how_will_you_attend"],
                        "email": row["email"],
                        "godhouse_location": row["godhouse_location"],
                        "need_accommodation": row["need_accommodation"],
                    },
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Imported attendee: {row["first_name"]} {row["last_name"]}'
                    )
                )
