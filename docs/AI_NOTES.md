# How I used AI

## Prompts

I used AI step by step, not all at once:

- Gave it the assessment PDF and asked it to explain what to build and break it into steps
- Asked for the requirements doc
- Asked for the Django model and a seed script for 10,000 employees
- Asked for the API (pagination, search, filters) and the insights
- Asked for the React UI with Ant Design
- Asked for unit tests

## What went wrong and how I fixed it

- The frontend gave a CORS error. I checked `settings.py` and fixed it myself.
- `views.py` had a missing import. I found it by reading the traceback.
- The first tests missed some cases, so I added tests for negative salary, duplicate email, even-count median, search, update and delete.

## What I verified myself

- Ran the seed script and checked the count is 10,000
- Ran all tests (15 pass)
- Opened the deployed app and checked that list, search and insights work

## Decisions I made

- Insights grouped by currency to avoid mixing INR and USD
- Aggregates in the DB, median in Python (SQLite has no median)
- Left out auth, payroll, currency conversion (see REQUIREMENTS.md)