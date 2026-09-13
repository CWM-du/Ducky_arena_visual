import re

from django.core.management.base import BaseCommand
from duckies.models import Item


def item_image_filename(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") + ".png"


CATALOG = [
    # HEAD
    {
        "name": "Corona del Alba",
        "image": "ducky_items/corona-del-alba.png",
        "item_type": "HEAD",
        "rarity": "LEGENDARY",
        "description": "Una corona ligera que simboliza el comienzo de una nueva aventura.",
    },
    {
        "name": "Capucha del Errante",
        "image": "ducky_items/capucha-del-errante.png",
        "item_type": "HEAD",
        "rarity": "COMMON",
        "description": "Una capucha sencilla para quienes prefieren viajar sin llamar la atención.",
    },
    {
        "name": "Yelmo de Guardián",
        "image": "ducky_items/yelmo-de-guardian.png",
        "item_type": "HEAD",
        "rarity": "RARE",
        "description": "Un yelmo reforzado que recuerda a los antiguos protectores del reino.",
    },
    {
        "name": "Diadema Astral",
        "image": "ducky_items/diadema-astral.png",
        "item_type": "HEAD",
        "rarity": "EPIC",
        "description": "Una diadema adornada con símbolos de constelaciones olvidadas.",
    },
    {
        "name": "Sombrero del Archimago",
        "image": "ducky_items/sombrero-del-archimago.png",
        "item_type": "HEAD",
        "rarity": "LEGENDARY",
        "description": "Un sombrero ceremonial reservado para maestros de las artes arcanas.",
    },

    # EYES
    {
        "name": "Monóculo del Sabio",
        "image": "ducky_items/monoculo-del-sabio.png",
        "item_type": "EYES",
        "rarity": "RARE",
        "description": "Una lente encantada que da aspecto de estudioso veterano.",
    },
    {
        "name": "Gafas de Explorador",
        "image": "ducky_items/gafas-de-explorador.png",
        "item_type": "EYES",
        "rarity": "COMMON",
        "description": "Prácticas gafas preparadas para mapas, ruinas y largas expediciones.",
    },
    {
        "name": "Visor de Cristal Lunar",
        "image": "ducky_items/visor-de-cristal-lunar.png",
        "item_type": "EYES",
        "rarity": "EPIC",
        "description": "Cristales plateados inspirados en las noches mágicas del viejo continente.",
    },
    {
        "name": "Máscara del Oráculo",
        "image": "ducky_items/mascara-del-oraculo.png",
        "item_type": "EYES",
        "rarity": "LEGENDARY",
        "description": "Una máscara ceremonial asociada a quienes dicen ver el futuro.",
    },
    {
        "name": "Lentes de Alquimista",
        "image": "ducky_items/lentes-de-alquimista.png",
        "item_type": "EYES",
        "rarity": "RARE",
        "description": "Lentes color ámbar utilizadas por artesanos de pociones y artefactos.",
    },

    # BODY
    {
        "name": "Túnica del Aprendiz",
        "image": "ducky_items/tunica-del-aprendiz.png",
        "item_type": "BODY",
        "rarity": "COMMON",
        "description": "La vestimenta tradicional de quien acaba de iniciar su camino.",
    },
    {
        "name": "Armadura de Bronce",
        "image": "ducky_items/armadura-de-bronce.png",
        "item_type": "BODY",
        "rarity": "COMMON",
        "description": "Protección resistente y sencilla para las primeras mazmorras.",
    },
    {
        "name": "Manto de Hoja Verde",
        "image": "ducky_items/manto-de-hoja-verde.png",
        "item_type": "BODY",
        "rarity": "RARE",
        "description": "Un manto de explorador inspirado en los bosques encantados.",
    },
    {
        "name": "Armadura del Caballero Solar",
        "image": "ducky_items/armadura-del-caballero-solar.png",
        "item_type": "BODY",
        "rarity": "EPIC",
        "description": "Una armadura ceremonial decorada con emblemas de un antiguo orden.",
    },
    {
        "name": "Túnica de Estrellas",
        "image": "ducky_items/tunica-de-estrellas.png",
        "item_type": "BODY",
        "rarity": "EPIC",
        "description": "Una túnica oscura salpicada de motivos que evocan un cielo nocturno.",
    },
    {
        "name": "Armadura del Dragón Celeste",
        "image": "ducky_items/armadura-del-dragon-celeste.png",
        "item_type": "BODY",
        "rarity": "LEGENDARY",
        "description": "Una armadura mítica con silueta inspirada en criaturas de los cielos.",
    },

    # ACCESSORY
    {
        "name": "Colgante del Valor",
        "image": "ducky_items/colgante-del-valor.png",
        "item_type": "ACCESSORY",
        "rarity": "RARE",
        "description": "Un pequeño talismán que representa el coraje ante lo desconocido.",
    },
    {
        "name": "Cristal de Maná",
        "image": "ducky_items/cristal-de-mana.png",
        "item_type": "ACCESSORY",
        "rarity": "EPIC",
        "description": "Un cristal luminoso usado como símbolo de energía mágica.",
    },
    {
        "name": "Capa de Viaje",
        "image": "ducky_items/capa-de-viaje.png",
        "item_type": "ACCESSORY",
        "rarity": "COMMON",
        "description": "Una capa compacta pensada para largas rutas y noches al aire libre.",
    },
    {
        "name": "Grimorio Miniatura",
        "image": "ducky_items/grimorio-miniatura.png",
        "item_type": "ACCESSORY",
        "rarity": "RARE",
        "description": "Un pequeño libro de hechizos que acompaña a los aventureros estudiosos.",
    },
    {
        "name": "Medallón del Fénix",
        "image": "ducky_items/medallon-del-fenix.png",
        "item_type": "ACCESSORY",
        "rarity": "LEGENDARY",
        "description": "Un medallón mítico asociado a la renovación y la perseverancia.",
    },
    {
        "name": "Brújula de las Ruinas",
        "image": "ducky_items/brujula-de-las-ruinas.png",
        "item_type": "ACCESSORY",
        "rarity": "EPIC",
        "description": "Una brújula antigua diseñada para quienes buscan secretos perdidos.",
    },
]


ARCANE_SETS = [
    # Each set has one item per equip slot.
    ("Arcano Python", "Python", [
        ("Sombrero Python", "HEAD", "LEGENDARY", "El sombrero del invocador de serpientes de código."),
        ("Lentes Python", "EYES", "EPIC", "Lentes que revelan scripts ocultos y caminos automáticos."),
        ("Túnica Python", "BODY", "RARE", "Una túnica flexible para maestros de la automatización."),
        ("Amuleto Python", "ACCESSORY", "LEGENDARY", "Un talismán que convierte ideas en hechizos ejecutables."),
    ]),
    ("Arcano JavaScript", "JavaScript", [
        ("Sombrero JavaScript", "HEAD", "EPIC", "Un sombrero eléctrico para tejedores de interfaces dinámicas."),
        ("Visor JavaScript", "EYES", "RARE", "Detecta eventos, callbacks y secretos del navegador."),
        ("Chaqueta JavaScript", "BODY", "LEGENDARY", "Una chaqueta cambiante, tan versátil como su lenguaje."),
        ("Pulsera JavaScript", "ACCESSORY", "EPIC", "Un brazalete que chisporrotea con cada evento disparado."),
    ]),
    ("Arcano Java", "Java", [
        ("Corona Java", "HEAD", "LEGENDARY", "Corona forjada para guardianes de la máquina virtual."),
        ("Gafas Java", "EYES", "RARE", "Observa objetos, clases y mundos encapsulados."),
        ("Armadura Java", "BODY", "EPIC", "Armadura robusta diseñada para aventuras multiplataforma."),
        ("Cristal Java", "ACCESSORY", "RARE", "Un cristal que mantiene la magia ejecutándose en cualquier reino."),
    ]),
    ("Arcano C++", "C++", [
        ("Yelmo C++", "HEAD", "LEGENDARY", "Un yelmo pesado para guerreros del rendimiento extremo."),
        ("Monóculo C++", "EYES", "EPIC", "Permite distinguir punteros, referencias y memoria oculta."),
        ("Armadura C++", "BODY", "LEGENDARY", "Una armadura precisa y poderosa, construida para durar."),
        ("Emblema C++", "ACCESSORY", "RARE", "Un emblema con la fuerza de generaciones de código."),
    ]),
    ("Arcano C#", "C#", [
        ("Diadema C#", "HEAD", "EPIC", "Diadema elegante para hechiceros del ecosistema .NET."),
        ("Visor C#", "EYES", "RARE", "Enfoca interfaces, objetos y mundos conectados."),
        ("Manto C#", "BODY", "EPIC", "Un manto pulido para aventureros de aplicaciones y juegos."),
        ("Medallón C#", "ACCESSORY", "LEGENDARY", "Medallón con el sello de los artesanos del código moderno."),
    ]),
    ("Arcano Rust", "Rust", [
        ("Capucha Rust", "HEAD", "RARE", "Capucha reforzada contra errores y peligros de memoria."),
        ("Lentes Rust", "EYES", "EPIC", "Permiten ver la seguridad antes de que llegue el peligro."),
        ("Armadura Rust", "BODY", "LEGENDARY", "Protección férrea para exploradores obsesionados con la seguridad."),
        ("Talismán Rust", "ACCESSORY", "EPIC", "Un talismán que mantiene la propiedad bajo control."),
    ]),
    ("Arcano Go", "Go", [
        ("Sombrero Go", "HEAD", "RARE", "Sombrero ligero para mensajeros de reinos concurrentes."),
        ("Gafas Go", "EYES", "COMMON", "Visión clara para recorrer servicios a toda velocidad."),
        ("Túnica Go", "BODY", "EPIC", "Túnica sencilla, rápida y preparada para grandes expediciones."),
        ("Brújula Go", "ACCESSORY", "RARE", "Encuentra rutas entre procesos, servidores y aventuras."),
    ]),
    ("Arcano Ruby", "Ruby", [
        ("Sombrero Ruby", "HEAD", "EPIC", "Un sombrero carmesí para artesanos de código elegante."),
        ("Gafas Ruby", "EYES", "RARE", "Lentes que resaltan soluciones limpias y expresivas."),
        ("Capa Ruby", "BODY", "LEGENDARY", "Una capa roja tejida con magia de productividad."),
        ("Gema Ruby", "ACCESSORY", "EPIC", "Una gema preciosa para quienes prefieren la elegancia."),
    ]),
    ("Arcano PHP", "PHP", [
        ("Capucha PHP", "HEAD", "COMMON", "Capucha clásica para viajeros de los antiguos portales web."),
        ("Visor PHP", "EYES", "RARE", "Ayuda a encontrar secretos escondidos tras cada petición."),
        ("Túnica PHP", "BODY", "EPIC", "Vestimenta de veterano de las grandes fortalezas web."),
        ("Pergamino PHP", "ACCESSORY", "LEGENDARY", "Un pergamino antiguo que conoce incontables rutas del servidor."),
    ]),
    ("Arcano Swift", "Swift", [
        ("Corona Swift", "HEAD", "LEGENDARY", "Una corona veloz para guardianes de mundos móviles."),
        ("Visor Swift", "EYES", "EPIC", "Visor cristalino para interfaces rápidas y precisas."),
        ("Armadura Swift", "BODY", "RARE", "Armadura ligera diseñada para moverse sin resistencia."),
        ("Pluma Swift", "ACCESSORY", "EPIC", "Una pluma arcana que convierte ideas en movimientos fluidos."),
    ]),
]

for set_name, language, pieces in ARCANE_SETS:
    for item_name, item_type, rarity, description in pieces:
        CATALOG.append({
            "name": item_name,
            "image": f"ducky_items/{item_image_filename(item_name)}",
            "item_type": item_type,
            "category": "ARCANO",
            "set_name": set_name,
            "rarity": rarity,
            "description": description,
        })


class Command(BaseCommand):
    help = "Populate the Ducky catalog with the approved MVP item catalog."

    def handle(self, *args, **options):
        created = 0
        updated = 0

        for data in CATALOG:
            item, was_created = Item.objects.update_or_create(
                name=data["name"],
                defaults={
                    "item_type": data["item_type"],
                    "category": data.get("category", "STANDARD"),
                    "set_name": data.get("set_name", ""),
                    "rarity": data["rarity"],
                    "description": data["description"],
                    "image": data["image"],
                    "is_active": True,
                },
            )
            if was_created:
                created += 1
                self.stdout.write(self.style.SUCCESS(f"Creado: {item.name}"))
            else:
                updated += 1
                self.stdout.write(f"Actualizado: {item.name}")

        self.stdout.write(
            self.style.SUCCESS(
                f"Catálogo cargado: {created} creados, {updated} actualizados, "
                f"{len(CATALOG)} registros definidos."
            )
        )
