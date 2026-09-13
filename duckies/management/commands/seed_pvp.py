from django.core.management.base import BaseCommand
from django.db import transaction

from duckies.models import Attack, Item, ItemResistance


ATTACK_IMAGES = {
    "Syntax Lock": "ducky_attacks/syntax-lock.png",
    "Freeze Process": "ducky_attacks/freeze-process.png",
    "Function Block": "ducky_attacks/function-block.png",
    "Code Scramble": "ducky_attacks/code-scramble.png",
    "Bug Injection": "ducky_attacks/bug-injection.png",
    "Fog of Code": "ducky_attacks/fog-of-code.png",
    "Runtime Delay": "ducky_attacks/runtime-delay.png",
    "Slow Compile": "ducky_attacks/slow-compile.png",
    "Infinite Loop": "ducky_attacks/infinite-loop.png",
    "Runtime Error": "ducky_attacks/runtime-error.png",
    "Refactor": "ducky_attacks/refactor.png",
    "Dependency Wall": "ducky_attacks/dependency-wall.png",
    "Event Loop": "ducky_attacks/event-loop.png",
    "Memory Guard": "ducky_attacks/memory-guard.png",
    "Borrow Check": "ducky_attacks/borrow-check.png",
    "Goroutine Rush": "ducky_attacks/goroutine-rush.png",
    "Optional Trap": "ducky_attacks/optional-trap.png",
    "Server Timeout": "ducky_attacks/server-timeout.png",
}


ATTACKS = [
    ("Syntax Lock", "Bloquea temporalmente el avance del rival.", "LOCK", 2, 8, 30, "", 1),
    ("Freeze Process", "Detiene durante unos segundos la acción de progreso.", "LOCK", 3, 5, 40, "", 2),
    ("Function Block", "Impide ejecutar una acción de avance del adversario.", "INTERRUPT", 2, 7, 35, "", 2),
    ("Code Scramble", "Complica temporalmente la lectura del siguiente reto.", "SCRAMBLE", 2, 10, 40, "", 2),
    ("Bug Injection", "Introduce una penalización temporal en el flujo del rival.", "SABOTAGE", 2, 12, 45, "", 2),
    ("Fog of Code", "Reduce la claridad del próximo desafío del adversario.", "SCRAMBLE", 3, 8, 50, "", 3),
    ("Runtime Delay", "Reduce temporalmente la velocidad de avance.", "SLOW", 2, 12, 35, "", 1),
    ("Slow Compile", "Hace más lenta la resolución de acciones del rival.", "SLOW", 3, 10, 45, "", 2),
    ("Infinite Loop", "Atrapa el flujo del rival en una interrupción temporal.", "INTERRUPT", 3, 6, 55, "", 3),
    ("Runtime Error", "Interrumpe el progreso inmediatamente.", "SABOTAGE", 3, 7, 55, "", 3),
    ("Refactor", "Desordena temporalmente una secuencia de avance.", "REDIRECT", 2, 9, 45, "Ruby", 2),
    ("Dependency Wall", "Bloquea una acción hasta que expire el efecto.", "LOCK", 3, 7, 50, "Java", 3),
    ("Event Loop", "Retrasa la siguiente ventana de progreso.", "SLOW", 3, 9, 45, "JavaScript", 2),
    ("Memory Guard", "Interfiere con una acción de progreso mediante control de memoria.", "INTERRUPT", 3, 6, 50, "C++", 3),
    ("Borrow Check", "Frena una secuencia insegura del rival.", "SLOW", 2, 11, 40, "Rust", 2),
    ("Goroutine Rush", "Desvía temporalmente el ritmo de ejecución rival.", "REDIRECT", 2, 8, 40, "Go", 2),
    ("Optional Trap", "Obliga a gestionar una interrupción temporal.", "INTERRUPT", 2, 8, 40, "Swift", 2),
    ("Server Timeout", "Corta temporalmente el flujo de avance.", "LOCK", 3, 6, 50, "PHP", 3),
]


# Item -> effect reductions. Values are intentionally moderate so a build
# can counter an attack without making PvP completely deterministic.
RESISTANCES = {
    "Corona del Alba": {"LOCK": 25, "SILENCE": 15},
    "Capucha del Errante": {"SLOW": 30, "REDIRECT": 20},
    "Yelmo de Guardián": {"LOCK": 35, "INTERRUPT": 20},
    "Diadema Astral": {"SCRAMBLE": 35, "REDIRECT": 20},
    "Sombrero del Archimago": {"SABOTAGE": 30, "SCRAMBLE": 20},
    "Monóculo del Sabio": {"SABOTAGE": 25, "SCRAMBLE": 30},
    "Gafas de Explorador": {"REDIRECT": 30, "SABOTAGE": 15},
    "Visor de Cristal Lunar": {"SCRAMBLE": 40, "SILENCE": 20},
    "Máscara del Oráculo": {"INTERRUPT": 35, "REDIRECT": 25},
    "Lentes de Alquimista": {"SABOTAGE": 40},
    "Túnica del Aprendiz": {"LOCK": 10, "SLOW": 10, "INTERRUPT": 10, "SCRAMBLE": 10, "SABOTAGE": 10},
    "Armadura de Bronce": {"LOCK": 20, "INTERRUPT": 20},
    "Manto de Hoja Verde": {"SLOW": 35, "REDIRECT": 25},
    "Armadura del Caballero Solar": {"LOCK": 30, "INTERRUPT": 30, "SABOTAGE": 20},
    "Túnica de Estrellas": {"SCRAMBLE": 35, "SILENCE": 30},
    "Armadura del Dragón Celeste": {"LOCK": 45, "INTERRUPT": 35, "SABOTAGE": 30},
    "Colgante del Valor": {"INTERRUPT": 25, "RESET": 25},
    "Cristal de Maná": {"SILENCE": 35, "SLOW": 20},
    "Capa de Viaje": {"SLOW": 40, "REDIRECT": 30},
    "Grimorio Miniatura": {"SCRAMBLE": 30, "SABOTAGE": 25},
    "Medallón del Fénix": {"SABOTAGE": 45, "RESET": 30},
    "Brújula de las Ruinas": {"REDIRECT": 45, "SCRAMBLE": 20},
}


ARCANE_RESISTANCES = {
    "Arcano Python": {"SCRAMBLE": 20, "SABOTAGE": 25, "INTERRUPT": 15, "REDIRECT": 10},
    "Arcano JavaScript": {"SLOW": 25, "INTERRUPT": 30, "REDIRECT": 25, "LOCK": 10},
    "Arcano Java": {"LOCK": 30, "INTERRUPT": 20, "SABOTAGE": 25, "RESET": 15},
    "Arcano C++": {"INTERRUPT": 35, "LOCK": 20, "SABOTAGE": 25, "SLOW": 10},
    "Arcano C#": {"REDIRECT": 30, "SCRAMBLE": 25, "INTERRUPT": 20, "SILENCE": 15},
    "Arcano Rust": {"SABOTAGE": 50, "INTERRUPT": 30, "LOCK": 20, "SCRAMBLE": 15},
    "Arcano Go": {"SLOW": 35, "REDIRECT": 35, "INTERRUPT": 20, "LOCK": 10},
    "Arcano Ruby": {"REDIRECT": 40, "SCRAMBLE": 30, "SABOTAGE": 15, "SLOW": 15},
    "Arcano PHP": {"LOCK": 30, "SABOTAGE": 35, "SLOW": 20, "SCRAMBLE": 15},
    "Arcano Swift": {"INTERRUPT": 30, "SLOW": 30, "SABOTAGE": 25, "REDIRECT": 20},
}


class Command(BaseCommand):
    help = "Carga los ataques PvP y las resistencias de los objetos defensivos."

    @transaction.atomic
    def handle(self, *args, **options):
        for row in ATTACKS:
            name, description, effect_type, power, duration, cooldown, language, difficulty = row
            Attack.objects.update_or_create(
                name=name,
                defaults={
                    "description": description,
                    "image": ATTACK_IMAGES[name],
                    "effect_type": effect_type,
                    "power": power,
                    "duration_seconds": duration,
                    "cooldown_seconds": cooldown,
                    "language": language,
                    "difficulty": difficulty,
                    "is_active": True,
                },
            )

        for item_name, effects in RESISTANCES.items():
            try:
                item = Item.objects.get(name=item_name)
            except Item.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"Objeto no encontrado: {item_name}"))
                continue
            for effect_type, reduction in effects.items():
                ItemResistance.objects.update_or_create(
                    item=item,
                    effect_type=effect_type,
                    defaults={"reduction_percent": reduction},
                )

        for set_name, effects in ARCANE_RESISTANCES.items():
            for item in Item.objects.filter(category="ARCANO", set_name=set_name):
                # Set resistance is applied to every equipped piece in the set.
                # A full four-piece set therefore creates a strong, but still
                # capped, defensive identity.
                for effect_type, reduction in effects.items():
                    ItemResistance.objects.update_or_create(
                        item=item,
                        effect_type=effect_type,
                        defaults={"reduction_percent": reduction // 4},
                    )

        self.stdout.write(self.style.SUCCESS("Sistema PvP cargado: 18 ataques, defensas estándar y resistencias Arcano."))
