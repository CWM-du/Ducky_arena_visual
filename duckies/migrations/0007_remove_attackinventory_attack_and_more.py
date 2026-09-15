from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("duckies", "0006_merge_20260914_0942"),
    ]

    operations = [
        migrations.RenameIndex(
            model_name="activeeffect",
            new_name="duckies_act_ducky_i_d25ffd_idx",
            old_name="duckies_act_ducky_i_7bb1f2_idx",
        ),
        migrations.RenameIndex(
            model_name="attack",
            new_name="duckies_att_effect__e92797_idx",
            old_name="duckies_att_effect_8e4d7f_idx",
        ),
        migrations.RenameIndex(
            model_name="attack",
            new_name="duckies_att_languag_639b47_idx",
            old_name="duckies_att_langua_47f7d6_idx",
        ),
        migrations.DeleteModel(
            name="AttackItem",
        ),
        migrations.DeleteModel(
            name="AttackInventory",
        ),
    ]
