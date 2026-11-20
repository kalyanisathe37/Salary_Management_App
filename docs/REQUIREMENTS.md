# Salary Management: Requirements

## Goal
HR Manager of ACME (10,000 employees, multiple countries) ko Excel ki jagah
ek web app dena, jisse wo salary data manage kare aur "hum kaise pay karte
hain" ke sawaalon ke jawab le sake.

## Scope & Features
1. Employee CRUD: name, email, job title, department, country, currency,
   salary, joining date
2. Employee list: server-side pagination, search, filter (country, job title)
3. Insights: min / max / avg / median salary by country and by job title,
   headcount per country
4. Seed script: 10,000 realistic employees
5. Validation: salary > 0, valid currency, unique email

## Deliberately Left Out (and why)
- Login/auth: assessment ka focus salary logic hai, single persona (HR).
  Production mein pehle add hoga.
- Payroll, tax, bonus, payslips: alag problem hai, scope badh jayega.
- Currency conversion (live rates): insights currency ke andar group hote
  hain, taaki galat comparison na ho. Conversion v2 mein.
- Excel import/export: nice-to-have, 3-hour limit mein nahi.
- Salary history/audit log: useful hai, par core question nahi.

## Key Decisions
- Aggregates DB mein (not in Python/JS) taaki 10k+ rows pe fast rahe
- Indexes on country, job_title
- Per-employee currency field (multi-country)