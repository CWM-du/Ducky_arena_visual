from django.urls import path

from . import views

app_name = "duckies"

urlpatterns = [
    path("", views.my_ducky, name="my_ducky"),
    path("rename/", views.rename_ducky, name="rename"),
    path("inventory/", views.inventory, name="inventory"),
    path("customize/", views.customize, name="customize"),
    path("equip/<int:pk>/", views.equip_item, name="equip"),
    path("unequip/<int:pk>/", views.unequip_item, name="unequip"),
]
