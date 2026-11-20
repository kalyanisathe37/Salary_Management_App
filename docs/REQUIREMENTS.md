# Salary Management: Requirements

## Goal
Give ACME's HR Manager (10,000 employees across multiple countries) a web app
to replace Excel, so they can manage salary data and answer questions about
how the organization pays its people.

## Scope & Features
1. Employee CRUD: name, email, job title, department, country, currency,
   salary, joining date
2. Employee list: server-side pagination, search, and filters (country, job title)
3. Insights: min / max / average / median salary by country and by job title,
   plus headcount
4. Seed script: 10,000 realistic employees
5. Validation: salary must be greater than 0, email must be unique

## Deliberately Left Out (and why)
- **Login/auth:** The assessment focuses on salary logic and there is a single
  persona (HR). It would be the first thing added for production.
- **Payroll, tax, bonus, payslips:** A separate problem that would inflate scope.
- **Currency conversion (live rates):** Insights are grouped within each
  currency so that unlike amounts are never compared. Conversion is a v2 item.
- **Excel import/export:** Nice to have, but outside the 3-hour limit.
- **Salary history / audit log:** Useful, but not needed to answer the core
  questions.

## Key Decisions
- Aggregates (count, min, max, avg) are computed in the database, not in
  Python/JS, so they stay fast at 10k+ rows.
- Indexes on `country` and `job_title`.
- Each employee has their own currency field (multi-country support).
- Insights are grouped by currency, because averaging INR and USD together
  would give a meaningless number.
- Median is computed in Python because SQLite has no built-in median. On
  Postgres we would use `percentile_cont`.
- SQLite is used for simplicity; production would use Postgres.