from decimal import Decimal
from datetime import date

from django.test import TestCase
from rest_framework.test import APIClient

from .insights import salary_stats
from .models import Employee


def make_employee(i, country="India", currency="INR", salary=100000, job_title="Engineer"):
    return Employee.objects.create(
        full_name=f"Person {i}",
        email=f"p{i}@acme.com",
        job_title=job_title,
        department="Engineering",
        country=country,
        currency=currency,
        salary=Decimal(salary),
        date_joined=date(2024, 1, 1),
    )


class InsightsTests(TestCase):
    def test_stats_for_one_country(self):
        for i, s in enumerate([100, 200, 600]):
            make_employee(i, salary=s)

        result = salary_stats("country")

        self.assertEqual(len(result), 1)
        row = result[0]
        self.assertEqual(row["count"], 3)
        self.assertEqual(row["min"], 100)
        self.assertEqual(row["max"], 600)
        self.assertEqual(row["avg"], 300)
        self.assertEqual(row["median"], 200)

    def test_countries_are_grouped_separately(self):
        make_employee(1, country="India", currency="INR", salary=100)
        make_employee(2, country="USA", currency="USD", salary=900)

        result = salary_stats("country")

        self.assertEqual({r["country"] for r in result}, {"India", "USA"})


class EmployeeApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_employee(self):
        payload = {
            "full_name": "Asha", "email": "asha@acme.com",
            "job_title": "Engineer", "department": "Engineering",
            "country": "India", "currency": "INR",
            "salary": "500000", "date_joined": "2024-01-01",
        }
        response = self.client.post("/api/employees/", payload, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Employee.objects.count(), 1)

    def test_rejects_zero_salary(self):
        payload = {
            "full_name": "Asha", "email": "asha@acme.com",
            "job_title": "Engineer", "department": "Engineering",
            "country": "India", "currency": "INR",
            "salary": "0", "date_joined": "2024-01-01",
        }
        response = self.client.post("/api/employees/", payload, format="json")
        self.assertEqual(response.status_code, 400)

    def test_filter_by_country(self):
        make_employee(1, country="India")
        make_employee(2, country="USA", currency="USD")

        response = self.client.get("/api/employees/?country=India")

        self.assertEqual(response.json()["count"], 1)

    def test_list_is_paginated(self):
        for i in range(60):
            make_employee(i)

        response = self.client.get("/api/employees/")

        self.assertEqual(len(response.json()["results"]), 50)
        self.assertEqual(response.json()["count"], 60)

class MoreInsightsTests(TestCase):
    def test_median_with_even_count(self):
        for i, s in enumerate([100, 200, 300, 400]):
            make_employee(i, salary=s)

        row = salary_stats("country")[0]

        self.assertEqual(row["median"], 250)

    def test_same_country_different_currency_not_mixed(self):
        make_employee(1, country="India", currency="INR", salary=100)
        make_employee(2, country="India", currency="USD", salary=100)

        result = salary_stats("country")

        self.assertEqual(len(result), 2)

    def test_stats_by_job_title(self):
        make_employee(1, job_title="Engineer", salary=100)
        make_employee(2, job_title="Manager", salary=500)

        result = salary_stats("job_title")

        self.assertEqual({r["job_title"] for r in result}, {"Engineer", "Manager"})


class MoreEmployeeApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.payload = {
            "full_name": "Asha", "email": "asha@acme.com",
            "job_title": "Engineer", "department": "Engineering",
            "country": "India", "currency": "INR",
            "salary": "500000", "date_joined": "2024-01-01",
        }

    def test_rejects_negative_salary(self):
        self.payload["salary"] = "-100"
        response = self.client.post("/api/employees/", self.payload, format="json")
        self.assertEqual(response.status_code, 400)

    def test_rejects_duplicate_email(self):
        make_employee(1)
        self.payload["email"] = "p1@acme.com"
        response = self.client.post("/api/employees/", self.payload, format="json")
        self.assertEqual(response.status_code, 400)

    def test_search_by_name(self):
        make_employee(1)
        make_employee(2)
        response = self.client.get("/api/employees/?search=Person 1")
        self.assertEqual(response.json()["count"], 1)

    def test_update_salary(self):
        emp = make_employee(1, salary=100)
        response = self.client.patch(
            f"/api/employees/{emp.id}/", {"salary": "200"}, format="json"
        )
        self.assertEqual(response.status_code, 200)
        emp.refresh_from_db()
        self.assertEqual(emp.salary, 200)

    def test_delete_employee(self):
        emp = make_employee(1)
        response = self.client.delete(f"/api/employees/{emp.id}/")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Employee.objects.count(), 0)

    def test_insights_endpoint_returns_200(self):
        make_employee(1)
        response = self.client.get("/api/insights/by-country/")
        self.assertEqual(response.status_code, 200)