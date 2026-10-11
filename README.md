# VNimavum

Online and in-store shop system for VNimavum, a small business that mainly sells
bedsheets and pillows, along with other items.

## What it does

- **Online storefront**: customers browse products and place orders.
- **Owner app**: the owner manages products, orders and physical stock, and
  uses its cashier checkout for sales in the physical shop. It is installed on
  the shop's Windows PC and keeps working when the internet is down.

Expected volume is under 100 orders a day, so the system is meant to stay simple
and run on one small server.

## Stack

| Part | Technology | Notes |
|------|------------|-------|
| Backend and owner interface | Django + Django REST Framework | Django admin covers product, stock and order management. |
| Customer storefront | Next.js (React) | Server rendering for search engines and fast page loads. |
| Database | PostgreSQL | |

The storefront talks to Django only through the REST API. The owner uses Django's
admin and never touches the React app.

```
Customer browser ──> Next.js storefront ──(REST API)──> Django + DRF ──> PostgreSQL
Owner browser    ──────────────────────> Django admin ──┘
```

## Repository layout

```
backend/            Django project (API, admin, in-store checkout sync)
  config/           Settings and URLs
  catalog/ ...      One Django app per module (see docs/architecture.md)
docs/               Architecture and data model
docker-compose.yml  Local PostgreSQL
```

Planned, not created yet: `owner-app/`, `storefront/`, `shared/ui`,
`shared/api-client`.

## Status

The backend has its database model and Django admin screens. There is no API,
owner app or storefront yet. See [docs/architecture.md](docs/architecture.md)
for the design and [CLAUDE.md](CLAUDE.md) for agreed decisions.

## Getting started (Windows, VS Code)

You need [Python 3.13](https://www.python.org/downloads/),
[Docker Desktop](https://www.docker.com/products/docker-desktop/) and VS Code.

1. Open the repository folder in VS Code and install the recommended
   extensions when asked.
2. Start the database (from the repository folder):
   ```
   docker compose up -d
   ```
3. Set up Python (from the `backend` folder):
   ```
   py -3.13 -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py createsuperuser
   ```
4. In VS Code, open Run and Debug and start **Django: run server**. Then open
   http://localhost:8000/admin/ and sign in with the user you just created.

Run the tests with **Django: run tests** in Run and Debug, or
`python manage.py test` from the `backend` folder.

The database settings default to the values in `docker-compose.yml`. To change
them, copy `backend/.env.example` to `backend/.env` and edit it.
