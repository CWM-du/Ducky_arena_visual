
## PvP: ataques y defensas

El sistema inicial de combate PvP está diseñado alrededor del **avance**, no de puntos de vida.
Un ataque correcto en un reto de programación puede aplicar temporalmente un efecto al rival:
bloqueo, lentitud, interrupción, código confuso, sabotaje, silencio, redirección o reinicio.

Las defensas proceden de los objetos equipados mediante `ItemResistance`. La resistencia reduce
el poder del efecto recibido; varias piezas pueden sumar resistencia hasta un máximo del 100%.
No se elimina inventario ni progreso de forma permanente.

### Artwork integrado

La versión actual incluye artwork RPG generado para todo el contenido visual integrado:

- 22 Items estándar.
- 40 Items Arcano (10 sets × 4 piezas).
- 18 ataques PvP, cada uno con `Attack.image`.
- 10 artworks de set Arcano.
- 8 iconos reutilizables de tipos de efecto defensivo.
- Catálogo visual consolidado en `static/duckies/ducky_item_catalog.png`.
- Resumen PvP en `static/duckies/ducky_pvp_catalog.png`.

Las imágenes de Items y ataques viven en `media/`, mientras que los recursos visuales
generales de sets y tipos defensivos viven en `static/`, siguiendo la separación
STATIC/MEDIA exigida por el enunciado.

### Cargar el sistema

```bash
python manage.py migrate
python manage.py seed_catalog
python manage.py seed_pvp
```

`seed_catalog` carga 62 Items (22 estándar + 40 Arcano). `seed_pvp` crea los 18 ataques
iniciales y relaciona los objetos defensivos con sus resistencias.

Los ataques con `language` permiten conectar posteriormente las habilidades con los retos
del lenguaje correspondiente.

