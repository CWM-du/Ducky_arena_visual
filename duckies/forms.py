from django import forms

from .models import Ducky, Item


class DuckyNameForm(forms.ModelForm):
    class Meta:
        model = Ducky
        fields = ["name"]
        labels = {"name": "Nombre del Ducky"}
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "maxlength": 50,
                    "autocomplete": "off",
                    "placeholder": "Ej. Byte",
                }
            )
        }

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if len(name) < 3:
            raise forms.ValidationError(
                "El nombre debe tener al menos 3 caracteres."
            )
        return name


class CustomizationForm(forms.Form):
    """
    Presents only items owned by the current Ducky.
    A blank value means that the category should be unequipped.
    """

    def __init__(self, *args, ducky, **kwargs):
        super().__init__(*args, **kwargs)
        self.ducky = ducky

        for item_type, label in Item.ItemType.choices:
            field_name = item_type.lower()
            choices = [("", "Ninguno")]
            choices.extend(
                (
                    str(inventory_item.pk),
                    inventory_item.item.name,
                )
                for inventory_item in (
                    ducky.inventory
                    .select_related("item")
                    .filter(item__item_type=item_type)
                    .order_by("item__name")
                )
            )
            self.fields[field_name] = forms.ChoiceField(
                label=label,
                choices=choices,
                required=False,
            )

    def clean(self):
        cleaned_data = super().clean()
        for item_type, _ in Item.ItemType.choices:
            field_name = item_type.lower()
            value = cleaned_data.get(field_name)
            if value:
                try:
                    inventory_item = self.ducky.inventory.select_related("item").get(
                        pk=value,
                        item__item_type=item_type,
                    )
                except Exception:
                    raise forms.ValidationError(
                        "La personalización contiene un objeto no válido."
                    )
                if not inventory_item.item.is_active:
                    raise forms.ValidationError(
                        "No puedes equipar un objeto que ya no está activo."
                    )
        return cleaned_data
