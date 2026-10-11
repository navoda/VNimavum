# CLAUDE.md

Instructions for Claude when working on this repository. Read this first.

## Working with the owner of this project

The developer wants to be hands-on. **Do not take creative liberty.**

- Ask before making any design, product, naming, data-model, UI or
  architecture decision that has not already been agreed and written down here.
- This includes choosing libraries, adding features, picking field names,
  writing marketing copy, choosing colours or layouts, and adding pages.
- When asking, give a short recommendation with the reason, then wait for an
  answer.
- Do only what was asked. Point out anything else worth doing, but do not do it.
- Once a decision is made, record it under "Agreed decisions" below so it is not
  asked again.

## Project summary

VNimavum is a small shop selling mainly bedsheets and pillows, plus other items.
It has an online store and a physical shop. Volume is under 100 orders a day.

Two parts:

1. **Customer storefront**: online browsing and ordering.
2. **Owner app**: manage products, orders and physical stock, including the
   in-store cashier checkout. Only the owner uses it; customers never touch the
   checkout. Online and in-store sales draw from the same stock.

## Agreed decisions

- Backend and owner interface: Django with Django REST Framework.
- Owner daily work (in-store checkout, stock, orders) happens in an owner app
  installed on the shop's Windows PC as an installable web app (PWA). It must
  keep working when the internet is down: it keeps a local copy and an outbox of
  sales and stock changes, and syncs to Django when online. The app asks the
  browser for persistent storage. Django admin stays as a back-office fallback.
- UI stays minimal for now; a unified look across the apps comes later.
- The codebase is split into modules for reuse and maintainability.
- Customer storefront: Next.js (React).
- The storefront talks to Django only through the REST API. The owner never uses
  the React app.
- Database: PostgreSQL.
- Both apps are hosted on one small server.
- Planned folders: `backend/` for Django, `storefront/` for Next.js.
- Online payments: Visa, Mastercard, bank transfer, PayPal.
- In-store payments: cash, bank transfer with a reference, and a bank card
  reader connected later. The owner app shows the day's cash total in the shop.
- Product categories (curtains, cushions, candles, bedsheets, pillows, etc.)
  define which variants a product has: size, colour or pattern, material.
- Delivery within Sri Lanka with fees shown, plus in-store pickup. Keep the
  design open to overseas delivery later.
- Storefront supports both guest checkout and customer accounts.
- Multiple currencies, converted using an online rate service updated daily.
  Primary currency: LKR. Rate service: Frankfurter (https://frankfurter.dev/),
  which carries Central Bank of Sri Lanka rates; the owner can override a rate.
- English only for now. No tax for now.
- Development: open and run in VS Code on localhost. PostgreSQL runs in
  Docker; Django and the apps run directly from VS Code. Production hosting on
  a private server later.
- Versions: use current long-term-support versions of the stack.
- One in-store device. Only in-store sales must work offline; everything else
  may require internet.
- When the last unit of a variant sells online, the owner app shows a
  notification. Overselling during an outage is accepted; the owner resolves
  it with the customer (for example, a refund).
- Online orders always require customer contact information.
- Backend module names: catalog, inventory, sales, payments, orders, delivery,
  currency, customers, sync, accounts. Frontend: owner-app/, storefront/,
  shared/ui, shared/api-client.

## Open decisions

Ask about these before working on anything that depends on them:

- Online card payment provider (gateway): keep open; the owner will research
  options later.

## Conventions

None agreed yet. Add them here as they are decided (code style, formatting,
tests, commit messages, branch naming).

## Commands

None yet. Add setup, run, test and lint commands here once the projects are
scaffolded.
