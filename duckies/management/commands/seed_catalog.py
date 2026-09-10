from django.core.management.base import BaseCommand

from duckies.models import Item


class Command(BaseCommand):
    help = "Create or update the starter Ducky Quiz Arenas catalog."

    ITEMS = [
        ("Sombrero Python", "HEAD", "RARE", "Sombrero de programador Python."),
        ("Gafas Hacker", "EYES", "COMMON", "Gafas pixel para el modo hacker."),
        ("Armadura SQL", "BODY", "EPIC", "Armadura inspirada en bases de datos."),
        ("Corona Regex", "HEAD", "LEGENDARY", "Corona para maestros de expresiones regulares."),
        ("Capa CSS", "BODY", "RARE", "Capa de estilo para tu Ducky."),
        ("Pulsera JavaScript", "ACCESSORY", "EPIC", "Accesorio de scripting."),
    ]

    def handle(self, *args, **options):
        for name, item_type, rarity, description in self.ITEMS:
            item, created = Item.objects.update_or_create(
                name=name,
                defaults={
                    "item_type": item_type,
                    "rarity": rarity,
                    "description": description,
                    "is_active": True,
                },
            )
            action = "Creado" if created else "Actualizado"
            self.stdout.write(self.style.SUCCESS(f"{action}: {item.name}"))
