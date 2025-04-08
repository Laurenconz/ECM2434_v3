from django.core.management.base import BaseCommand
from django.core.management import call_command
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Loads initial bingo tasks from initial_data.json'

    def handle(self, *args, **options):
        path = os.path.join(settings.BASE_DIR, 'bingo', 'initial_data.json')
        if os.path.exists(path):
            self.stdout.write(f"Loading data from {path}...")
            call_command('loaddata', path)
            self.stdout.write(self.style.SUCCESS("Initial bingo tasks loaded!"))
        else:
            self.stdout.write(self.style.ERROR("initial_data.json not found."))
