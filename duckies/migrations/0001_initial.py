from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Ducky",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(default="Ducky", max_length=50)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("owner", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="ducky", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["name", "id"]},
        ),
        migrations.CreateModel(
            name="Item",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField(blank=True)),
                ("item_type", models.CharField(choices=[("HEAD", "Cabeza"), ("EYES", "Ojos"), ("BODY", "Cuerpo"), ("ACCESSORY", "Accesorio")], max_length=20)),
                ("rarity", models.CharField(choices=[("COMMON", "Común"), ("RARE", "Raro"), ("EPIC", "Épico"), ("LEGENDARY", "Legendario")], default="COMMON", max_length=20)),
                ("image", models.ImageField(blank=True, null=True, upload_to="ducky_items/")),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["name", "id"]},
        ),
        migrations.CreateModel(
            name="InventoryItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("equipped", models.BooleanField(default=False)),
                ("obtained_at", models.DateTimeField(auto_now_add=True)),
                ("ducky", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="inventory", to="duckies.ducky")),
                ("item", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="owners", to="duckies.item")),
            ],
            options={"ordering": ["-equipped", "-obtained_at", "item__name"]},
        ),
        migrations.AddConstraint(
            model_name="inventoryitem",
            constraint=models.UniqueConstraint(fields=("ducky", "item"), name="unique_item_per_ducky"),
        ),
        migrations.AddIndex(
            model_name="item",
            index=models.Index(fields=["item_type", "is_active"], name="duckies_ite_item_ty_0f9b76_idx"),
        ),
        migrations.AddIndex(
            model_name="item",
            index=models.Index(fields=["rarity", "is_active"], name="duckies_ite_rarity_5d7a8e_idx"),
        ),
        migrations.AddIndex(
            model_name="inventoryitem",
            index=models.Index(fields=["ducky", "equipped"], name="duckies_inv_ducky_i_5bcd0e_idx"),
        ),
    ]
