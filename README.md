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

Planned, not created yet:

```
backend/      Django project (API, admin, in-store checkout)
storefront/   Next.js app for customers
```

## Status

The project has just been set up and contains documentation only. No code has
been written yet. Decisions still to be made are listed under "Open decisions"
in [CLAUDE.md](CLAUDE.md).

## Getting started

Setup steps will be added here once the backend and storefront are scaffolded.
