from django.core.management.base import BaseCommand
from bingo.models import Task
import json, os
from django.conf import settings

class Command(BaseCommand):
    help = 'Load bingo tasks from initial_data.json'

    def handle(self, *args, **kwargs):
        path = os.path.join(settings.BASE_DIR, 'bingo', 'initial_data.json')
        if not os.path.exists(path):
            self.stdout.write(self.style.ERROR(f" File not found: {path}"))
            return

        with open(path, 'r') as f:
            data = json.load(f)

        created = 0
        for entry in data:
            fields = entry['fields']
            obj, was_created = Task.objects.get_or_create(
                description=fields['description'],
                defaults={
                    'points': fields['points'],
                    'requires_upload': fields['requires_upload'],
                    'requires_scan': fields['requires_scan'],
                }
            )
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(f" Loaded {created} new bingo tasks."))
