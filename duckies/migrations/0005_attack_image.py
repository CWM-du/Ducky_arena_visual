from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("duckies", "0004_attack_itemresistance_activeeffect"),
    ]

    operations = [
        migrations.AddField(
            model_name="attack",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="ducky_attacks/",
            ),
        ),
    ]
