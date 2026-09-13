# Ducky Quiz Arenas — TODO

> Estado revisado contra el enunciado `TDA_Equip 3.pdf` y contra la versión actual del proyecto.
> Las tareas marcadas como completadas tienen implementación presente en el ZIP; las tareas de
> ejecución manual/verificación externa permanecen pendientes si no se han podido ejecutar.

## Before integration
- [x] Confirm the exact `accounts.User` implementation and `AUTH_USER_MODEL` value with the host project.
- [x] Confirm whether Ducky creation occurs in `accounts` during registration or lazily on `/ducky/`. This project uses lazy `get_or_create()` and does not implement a second creation mechanism.
- [x] Confirm shared base template/navigation with the other teams.

## MVP verification — PDF
- [x] Modelo `Ducky` implementado con `OneToOneField` hacia `settings.AUTH_USER_MODEL`.
- [x] Modelo `Item` implementado.
- [x] Modelo `InventoryItem` implementado.
- [x] Relación `Ducky` → `InventoryItem` → `Item`.
- [x] `ItemType` con `HEAD`, `EYES`, `BODY`, `ACCESSORY`.
- [x] `Rarity` con `COMMON`, `RARE`, `EPIC`, `LEGENDARY`.
- [x] `UniqueConstraint(Ducky, Item)`.
- [x] Migraciones del sistema de Duckies estructuradas.
- [x] Catálogo administrable en Django Admin.
- [x] Seed command implementado.
- [x] Catálogo aprobado cargado: 22 Items estándar + 40 Items Arcano.
- [x] Artwork individual integrado para los 62 Items.
- [x] 10 sets Arcano implementados (40 Items, 4 por set).
- [x] Ducky lazy `get_or_create()` implementado.
- [x] Cambio de nombre con formulario y validación mínima.
- [x] Inventario propio del usuario.
- [x] Filtros del inventario por categoría.
- [x] Equipar objeto.
- [x] Desequipar objeto.
- [x] Sustitución automática del objeto equipado de la misma categoría.
- [x] Acciones de equipar/desequipar protegidas mediante POST.
- [x] CSRF en formularios POST.
- [x] Seguridad de ownership mediante `ducky__owner=request.user`.
- [x] `transaction.atomic()` en las operaciones de negocio correspondientes.
- [x] Templates basados en `base.html`.
- [x] CSS correcto conectado mediante `duckies/css/app.css`.
- [x] Mi Ducky muestra visualmente las imágenes del equipamiento actual por categoría.
- [x] Imágenes separadas entre STATIC y MEDIA.
- [x] Mensajes de éxito/error en las operaciones principales.
- [x] Tests automatizados para modelos, inventario, equipamiento y seguridad presentes en `duckies/tests/`.
- [ ] Ejecutar `python manage.py check --deploy`.
- [ ] Ejecutar `python manage.py test duckies`.
- [ ] Ejecutar pruebas manuales de ownership con dos usuarios reales.
- [ ] Probar layouts mobile/tablet/desktop.
- [ ] Probar navegación por teclado y estados de foco visibles.

## Integration — PDF
- [ ] Acordar el contrato final de `Item` con `shop`.
- [x] Exponer `duckies.services.grant_item()` para que otros módulos puedan conceder Items sin duplicar modelos.
- [ ] Integrar concesión real de Items desde quiz/rewards cuando existan esos módulos.
- [ ] Añadir tests de integración cuando `shop` y reward apps existan.

## PvP extension — fuera del alcance obligatorio del PDF
- [x] Modelo `Attack` para efectos temporales de avance PvP.
- [x] `ItemResistance` para defensas/resistencias de los Items equipados.
- [x] `ActiveEffect` para efectos temporales aplicados al rival.
- [x] 18 ataques PvP definidos.
- [x] Resistencias estándar y resistencias asociadas a los 10 sets Arcano.
- [x] Lógica `resolve_attack()` con mitigación y límite del 100%.
- [x] Tests de mitigación, inmunidad, acumulación y expiración.
- [x] Artwork individual de los 18 ataques.
- [x] Artwork de los 10 sets Arcano.
- [x] Iconografía de los 8 tipos de efecto defensivo.
- [ ] Pantalla/arena PvP de combate.
- [ ] Integrar los ataques con retos de programación reales.
- [ ] Gestionar cooldowns y cargas de ataque desde una partida PvP.
- [ ] Mostrar efectos activos y resistencias en la interfaz de combate.
- [ ] Tests end-to-end del flujo reto → ataque → defensa → efecto.

## Production
- [ ] Configure production secret and allowed hosts.
- [ ] Configure HTTPS.
- [ ] Choose persistent database infrastructure.
- [ ] Choose persistent media storage.
- [ ] Deploy ASGI/WSGI behind a production application server.
- [ ] Configure monitoring/logging.

## Optional post-MVP — PDF
- [ ] Starter item.
- [ ] Randomized starter Ducky.
- [ ] Favorites.
- [x] Item sets — implementados mediante los 10 sets Arcano.
- [ ] Challenge-only achievement items.
- [ ] Preview before equip.
- [ ] Background category.
- [ ] Visual effects.
- [ ] Pets.
- [ ] Level requirements.
