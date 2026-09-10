# Ducky Quiz Arenas — TODO

## Before integration
- [X] Confirm the exact `accounts.User` implementation and `AUTH_USER_MODEL` value with the host project.
- [X] Confirm whether Ducky creation occurs in `accounts` during registration or lazily on `/ducky/`. This project uses lazy `get_or_create()` and does not implement a second creation mechanism.
- [X] Confirm shared base template/navigation with the other teams.

## MVP verification
- [ ] Populate the catalog with approved Item records.
- [ ] Upload final Item artwork.
- [ ] Run `python manage.py check --deploy`.
- [ ] Run `python manage.py test duckies`.
- [ ] Test ownership isolation with two real users.
- [ ] Test mobile/tablet/desktop layouts.
- [ ] Test keyboard navigation and visible focus states.

## Integration
- [ ] Agree on the `Item` contract with `shop`.
- [ ] Integrate quiz/reward Item grants through `duckies.services.grant_item`.
- [ ] Add integration tests once `shop` and reward apps exist.

## Production
- [ ] Configure production secret and allowed hosts.
- [ ] Configure HTTPS.
- [ ] Choose persistent database infrastructure.
- [ ] Choose persistent media storage.
- [ ] Deploy ASGI/WSGI behind a production application server.
- [ ] Configure monitoring/logging.

## Optional post-MVP
- [ ] Starter item.
- [ ] Randomized starter Ducky.
- [ ] Favorites.
- [ ] Item sets.
- [ ] Challenge-only achievement items.
- [ ] Preview before equip.
- [ ] Background category.
- [ ] Visual effects.
- [ ] Pets.
- [ ] Level requirements.
