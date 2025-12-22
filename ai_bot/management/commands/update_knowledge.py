from django.core.management.base import BaseCommand
from django.conf import settings
from ai_bot.models import KnowledgeBase
from ai_bot.services import VectorService
import os
from pathlib import Path


class Command(BaseCommand):
    help = "Reloads knowledge base from markdown files"

    def handle(self, *args, **options):
        self.stdout.write("Cleaning up old knowledge...")
        KnowledgeBase.objects.all().delete()

        kb_path = Path(settings.BASE_DIR) / 'ai_bot' / 'knowledge'

        service = VectorService()

        for filename in os.listdir(kb_path):
            if filename.endswith(".md"):
                self.stdout.write(f"Processing {filename}...")
                with open(os.path.join(kb_path, filename), 'r') as f:
                    content = f.read()
                    # Tutaj wywołujesz swoją logikę zapisu do bazy
                    service.update_knowledge(source=filename, content=content)

        self.stdout.write(self.style.SUCCESS("Successfully updated knowledge base!"))