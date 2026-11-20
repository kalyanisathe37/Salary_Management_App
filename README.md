# ACME Salary Management

A web app for the HR Manager of ACME to manage salaries of 10,000 employees across countries, and to answer questions like "how do we pay people?". It replaces the Excel sheets HR uses today.

## What it does

- Add, edit, delete and view employees
- Search and filter by country and job title, with pagination
- Insights by country and by job title: min, max, average, median salary and headcount
- Insights are grouped by currency so INR and USD never get mixed
- Salary must be greater than 0 and email must be unique
- Seed script that creates 10,000 employees

## Stack

Django + Django REST Framework, SQLite, React (Vite) and Ant Design.

## Running it locally

Backend:

```bash
python -m venv env
env\Scripts\activate        # on Mac/Linux: source env/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_employees
python manage.py runserver
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Then open http://localhost:5173

## Tests

```bash
python manage.py test
```

## API

- `GET, POST /api/employees/` (supports `?search=`, `?country=`, `?job_title=`, `?page=`)
- `GET, PUT, DELETE /api/employees/<id>/`
- `GET /api/insights/by-country/`
- `GET /api/insights/by-job-title/`

## Design decisions

- Count, min, max and average are calculated in the database so they stay fast with 10k rows.
- Median is calculated in Python because SQLite has no median function.
- Indexes on `country` and `job_title`.
- I left out auth, payroll and currency conversion on purpose. The reasons are in the docs below.

More details:
- [Requirements](docs/REQUIREMENTS.md)
- [How I used AI](docs/AI_NOTES.md)