# Ecom

A simple e-commerce site built with Django: a product listing, product detail pages, and a cart.

## Setup

Requires Python 3.12+.

```bash
python -m venv env
# Windows
env\Scripts\activate
# macOS / Linux
source env/bin/activate

pip install -r requirements.txt

cd Ecom
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/. Add products in the admin at http://127.0.0.1:8000/admin/.

## Configuration

Settings are read from environment variables. The defaults are fine for local development.

| Variable | Default | Purpose |
| --- | --- | --- |
| `DJANGO_SECRET_KEY` | insecure dev key | Set a real secret in production |
| `DJANGO_DEBUG` | `True` | Set to `False` in production |
| `DJANGO_ALLOWED_HOSTS` | empty | Comma-separated hostnames, e.g. `example.com,www.example.com` |

## Project layout

- `Ecom/Ecom/` – project settings and root URLs
- `Ecom/MyEcom/` – products, listing and detail pages
- `Ecom/cart/` – cart app
