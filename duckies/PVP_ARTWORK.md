# Artwork PvP y Arcano

Esta versión integra el artwork generado con el mismo lenguaje visual RPG del catálogo.

## Contenido

- 18 imágenes de ataques en `media/ducky_attacks/`.
- 40 imágenes individuales de Items Arcano en `media/ducky_items/`.
- 10 imágenes de conjunto en `static/duckies/arcano_sets/`.
- 8 iconos de tipo de efecto/defensa en `static/duckies/defenses/`.
- Catálogo general en `static/duckies/ducky_item_catalog.png`.
- Resumen del sistema PvP en `static/duckies/ducky_pvp_catalog.png`.

## Convención

Los Items y ataques son datos de la aplicación y por ello usan `MEDIA_ROOT`.
Los artworks de set y de tipos de efecto son recursos generales de la interfaz y usan `STATIC`.

Las defensas del sistema no se modelan como copias de Items: `ItemResistance` expresa la
resistencia de un Item equipado frente a un tipo de efecto PvP. Los iconos de `defenses/`
representan visualmente esos tipos de efecto y no crean un segundo modelo de defensa.
