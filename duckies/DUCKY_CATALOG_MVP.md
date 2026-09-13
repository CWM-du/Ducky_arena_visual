# Catálogo MVP de Ducky

Catálogo original para un juego de personalización RPG.

La dirección creativa toma referencias generales del género JRPG/fantasía de aventuras
(por ejemplo, sensación de exploración, reliquias, órdenes de caballería, magia y rarezas),
pero los nombres y conceptos son originales y no reproducen personajes, objetos o marcas
concretas de otras franquicias.

## Distribución

- HEAD: 5
- EYES: 5
- BODY: 6
- ACCESSORY: 6
- Total: 22

## Rareza

- COMMON: objetos básicos.
- RARE: objetos de exploración o especialización.
- EPIC: objetos con identidad visual fuerte.
- LEGENDARY: objetos aspiracionales y de colección.

## Carga

```powershell
python manage.py seed_catalog
```

El comando es idempotente: puede ejecutarse varias veces sin duplicar los registros.


## Sets especiales — Categoría Arcano

Se añaden 10 sets temáticos inspirados en lenguajes de programación, con 4 piezas
por set (HEAD, EYES, BODY y ACCESSORY):

1. Arcano Python
2. Arcano JavaScript
3. Arcano Java
4. Arcano C++
5. Arcano C#
6. Arcano Rust
7. Arcano Go
8. Arcano Ruby
9. Arcano PHP
10. Arcano Swift

Total adicional: **40 Items Arcano**. La categoría `ARCANO` se almacena separada
del slot de equipamiento (`item_type`), por lo que los cuatro slots originales siguen
funcionando igual. `set_name` identifica el conjunto al que pertenece cada pieza.

Las piezas Arcano se crean sin artwork en esta iteración para no confundir arte
conceptual con artwork final aprobado.
