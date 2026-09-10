from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("duckies", "0002_rename_duckies_inv_ducky_i_5bcd0e_idx_duckies_inv_ducky_i_b17c39_idx_and_more")]
    operations = [
        migrations.AddField(
            model_name="item", name="category",
            field=models.CharField(choices=[("STANDARD", "Estándar"), ("ARCANO", "Arcano")], default="STANDARD", max_length=20),
        ),
        migrations.AddField(
            model_name="item", name="set_name",
            field=models.CharField(blank=True, default="", max_length=100),
        ),
        migrations.AddIndex(
            model_name="item",
            index=models.Index(fields=["category", "set_name", "is_active"], name="duckies_ite_categor_5e5d4c_idx"),
        ),
    ]
