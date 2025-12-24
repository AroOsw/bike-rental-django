from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import BikeModel
from pathlib import Path


class Command(BaseCommand):
    help = "Update knowledgebase with current bike fleet"

    def handle(self, *args, **kwargs):
        kb_path = Path(settings.BASE_DIR) / "ai_bot" / "knowledge"
        file_path = kb_path / "bike-details.md"

        bikemodels = BikeModel.objects.all()

        with open(file_path, "w", encoding='utf-8') as f:
            f.write("# WildWheel Current Bike Fleet and Rental Offer\n\n"
                    "Size selection: If the customer has not provided a size,"
                    "ask for their height in centimeters and recommend the appropriate frame size (e.g. 175–185 cm = L).\n"
                    "Up-selling: If the customer asks about renting a bike for 2 days, mention that rentals of 3 days or more receive a 10% discount."
                    "## COMPLETENESS RULE: If the user asks about availability (e.g. a specific size or type), "
                    "search the entire catalog and list ALL matching models. Never limit the response to a single option "
                    "if more matching items exist in the database.\n\n")

            for model in bikemodels:
                get_description = model.get_ai_description()
                sizes = ", ".join(model.available_sizes) if model.available_sizes else "None available"

                f.write(f"{get_description} \n**Available sizes:** {sizes}\n")
                f.write("-" * 20 + "\n\n")

                self.stdout.write(self.style.SUCCESS(f"New bike {model.brand}-{model.model} added"))

            self.stdout.write(self.style.SUCCESS("Successfully updated knowledge base!"))
