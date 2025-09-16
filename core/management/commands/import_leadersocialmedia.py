import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import Leader, LeaderSocialMedia

class Command(BaseCommand):
    help = 'Import leader social media data from CSV'

    def handle(self, *args, **options):
        csv_file_path = os.path.join(settings.BASE_DIR, 'mygeodata', 'db', 'core_leadersocialmedia.csv')
        if not os.path.exists(csv_file_path):
            self.stdout.write(self.style.ERROR('CSV file not found'))
            return

        with open(csv_file_path, 'r') as file:
            reader = csv.DictReader(file)
            leaders_data = {}
            for row in reader:
                leader_id = int(row['leader_id'])
                if leader_id not in leaders_data:
                    leaders_data[leader_id] = {'social_media': []}
                leaders_data[leader_id]['social_media'].append({
                    'socialMediaName': row['socialMediaName'],
                    'link': row['link']
                })

        for leader_id, data in leaders_data.items():
            # Parse name from the first link
            first_link = data['social_media'][0]['link']
            username = self.parse_username(first_link)
            name = self.format_name(username)

            leader, created = Leader.objects.get_or_create(
                id=leader_id,
                defaults={
                    'name': name,
                    'position': 'Pastor',  # dummy
                    'bio': 'Bio not provided',  # dummy
                    'images': ''  # empty
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created leader: {name}'))

            for sm in data['social_media']:
                LeaderSocialMedia.objects.get_or_create(
                    leader=leader,
                    socialMediaName=sm['socialMediaName'],
                    link=sm['link']
                )
                self.stdout.write(self.style.SUCCESS(f'Created social media for {name}: {sm["socialMediaName"]}'))

    def parse_username(self, link):
        # Extract username from link
        if 'facebook.com/' in link:
            parts = link.split('facebook.com/')
            if len(parts) > 1:
                username = parts[1].split('?')[0].split('/')[0]
                return username
        elif 'instagram.com/' in link:
            parts = link.split('instagram.com/')
            if len(parts) > 1:
                username = parts[1].split('?')[0].split('/')[0]
                return username
        return 'Unknown'

    def format_name(self, username):
        # Simple formatting: replace dots and underscores with spaces, capitalize
        name = username.replace('.', ' ').replace('_', ' ').title()
        return name
