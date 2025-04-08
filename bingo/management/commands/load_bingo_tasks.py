from django.core.management.base import BaseCommand
from bingo.models import Task
import json, os
from django.conf import settings
print("Using DB engine:", settings.DATABASES['default']['ENGINE'])


class Command(BaseCommand):
    help = 'Load bingo tasks from initial_data.json'

    def handle(self, *args, **kwargs):
        path = os.path.join(settings.BASE_DIR, 'bingo', 'initial_data.json')
        if not os.path.exists(path):
            self.stdout.write(self.style.ERROR(f" File not found: {path}"))
            return

        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # clear existing tasks
        Task.objects.all().delete()

        created = 0
        for entry in data:
            fields = entry['fields']
            Task.objects.create(
                id=entry['pk'],
                description=fields['description'],
                points=fields['points'],
                requires_upload=fields['requires_upload'],
                requires_scan=fields['requires_scan']
            )
            created += 1

        self.stdout.write(self.style.SUCCESS(f" Reloaded {created} bingo tasks."))
