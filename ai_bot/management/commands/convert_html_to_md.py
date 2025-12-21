import os
import re
from django.conf import settings
from django.core.management.base import BaseCommand
from markdownify import markdownify as md
from pathlib import Path

class Command(BaseCommand):
    help = 'Converts HTML templates to Markdown files for AI knowledge base'

    def handle(self, *args, **options):

        template_dir = Path(settings.BASE_DIR) / 'core' / 'templates'
        output_dir = Path(settings.BASE_DIR) / 'ai_bot' / 'knowledge'

        # Sprawdźmy dla pewności w konsoli, czy ścieżka istnieje
        if not template_dir.exists():
            self.stdout.write(self.style.ERROR(f'Directory not found: {template_dir}'))
            return

        for filename in os.listdir(template_dir):
            if filename.endswith(".html"):
                with open(os.path.join(template_dir, filename), 'r', encoding='utf-8') as f:
                    html_content = f.read()

                # Usuwamy znaczniki skryptów i ich zawartość przed konwersją
                clean_html = re.sub(r'<script\b[^>]*>([\s\S]*?)<\/script>', '', html_content, flags=re.IGNORECASE)

                # Usuwamy tagi Django
                clean_html = re.sub(r'\{%.*?%\}', '', clean_html, flags=re.DOTALL)
                clean_html = re.sub(r'\{\{.*?\}\}', '', clean_html, flags=re.DOTALL)

                # Konwersja z wyłączeniem zbędnych tagów wizualnych
                markdown_text = md(
                    clean_html,
                    heading_style="ATX",
                    strip=['a', 'script', 'style', 'img', 'button']  # Dodajemy przyciski i obrazki do usunięcia
                )

                # 3. Zapis do nowego pliku
                new_filename = filename.replace(".html", ".md")
                with open(os.path.join(output_dir, new_filename), 'w', encoding='utf-8') as f:
                    f.write(markdown_text)

                self.stdout.write(self.style.SUCCESS(f'Converted: {filename} -> {new_filename}'))
