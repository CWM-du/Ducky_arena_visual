# Integración de Duckies

La app `duckies` se integra en el proyecto Django principal.

- `accounts` mantiene el `User` estándar de Django.
- No se usa `AUTH_USER_MODEL = "accounts.User"`.
- `duckies.Ducky.owner` utiliza `settings.AUTH_USER_MODEL`, que resuelve a `auth.User`.
- Las URLs de Duckies se exponen bajo `/duckies/`.

Ejecuta desde este directorio:

```powershell
python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
