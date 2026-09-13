from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [("duckies", "0003_item_category_set_name")]

    operations = [
        migrations.CreateModel(
            name="Attack",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField(blank=True)),
                ("effect_type", models.CharField(choices=[("LOCK", "Bloqueo"), ("SLOW", "Lentitud"), ("INTERRUPT", "Interrupción"), ("SCRAMBLE", "Código confuso"), ("SABOTAGE", "Sabotaje"), ("SILENCE", "Silencio"), ("REDIRECT", "Redirección"), ("RESET", "Reinicio")], max_length=20)),
                ("power", models.PositiveSmallIntegerField(default=1)),
                ("duration_seconds", models.PositiveIntegerField(default=10)),
                ("cooldown_seconds", models.PositiveIntegerField(default=30)),
                ("language", models.CharField(blank=True, default="", max_length=50)),
                ("difficulty", models.PositiveSmallIntegerField(default=1)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={"ordering": ["name", "id"], "indexes": [models.Index(fields=["effect_type", "is_active"], name="duckies_att_effect_8e4d7f_idx"), models.Index(fields=["language", "is_active"], name="duckies_att_langua_47f7d6_idx")]},
        ),
        migrations.CreateModel(
            name="ItemResistance",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("effect_type", models.CharField(choices=[("LOCK", "Bloqueo"), ("SLOW", "Lentitud"), ("INTERRUPT", "Interrupción"), ("SCRAMBLE", "Código confuso"), ("SABOTAGE", "Sabotaje"), ("SILENCE", "Silencio"), ("REDIRECT", "Redirección"), ("RESET", "Reinicio")], max_length=20)),
                ("reduction_percent", models.PositiveSmallIntegerField(default=0)),
                ("notes", models.CharField(blank=True, max_length=255)),
                ("item", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="resistances", to="duckies.item")),
            ],
            options={"ordering": ["item__name", "effect_type"], "constraints": [models.UniqueConstraint(fields=("item", "effect_type"), name="unique_item_resistance_type")]},
        ),
        migrations.CreateModel(
            name="ActiveEffect",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("effect_type", models.CharField(choices=[("LOCK", "Bloqueo"), ("SLOW", "Lentitud"), ("INTERRUPT", "Interrupción"), ("SCRAMBLE", "Código confuso"), ("SABOTAGE", "Sabotaje"), ("SILENCE", "Silencio"), ("REDIRECT", "Redirección"), ("RESET", "Reinicio")], max_length=20)),
                ("power", models.PositiveSmallIntegerField(default=1)),
                ("expires_at", models.DateTimeField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("attack", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="applied_effects", to="duckies.attack")),
                ("ducky", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="active_effects", to="duckies.ducky")),
            ],
            options={"ordering": ["expires_at", "-created_at"], "indexes": [models.Index(fields=["ducky", "effect_type", "expires_at"], name="duckies_act_ducky_i_7bb1f2_idx")]},
        ),
    ]
