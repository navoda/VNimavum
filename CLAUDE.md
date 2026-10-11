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

Three parts:

1. **Customer storefront**: online browsing and ordering.
2. **Owner interface**: manage products, orders and physical stock.
3. **In-store checkout**: the owner records sales made in the physical shop.
   Online and in-store sales draw from the same stock.

## Agreed decisions

- Backend and owner interface: Django with Django REST Framework.
- Owner screens use the Django admin wherever it is good enough, keeping custom
  code to a minimum.
- Customer storefront: Next.js (React).
- The storefront talks to Django only through the REST API. The owner never uses
  the React app.
- Database: PostgreSQL.
- Both apps are hosted on one small server.
- Planned folders: `backend/` for Django, `storefront/` for Next.js.

## Open decisions

Ask about these before working on anything that depends on them:

- How "offline" in-store checkout must be: does it need to work without an
  internet connection, or only without the customer being online?
- Payment methods for online orders, and which payment provider.
- Payment methods recorded for in-store sales (cash, card, other).
- Product data: variants (size, colour, material), images, categories.
- Delivery: areas, fees, and whether click-and-collect is offered.
- Customer accounts or guest checkout only.
- Currency, language(s) and tax rules.
- Python, Django, Node and Next.js versions; package managers.
- Hosting provider and deployment method.
- Whether to use Docker for local development.

## Conventions

None agreed yet. Add them here as they are decided (code style, formatting,
tests, commit messages, branch naming).

## Commands

None yet. Add setup, run, test and lint commands here once the projects are
scaffolded.
