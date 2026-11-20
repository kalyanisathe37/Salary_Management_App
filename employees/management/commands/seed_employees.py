import random
from datetime import timedelta, date
from decimal import Decimal

from django.core.management.base import BaseCommand
from faker import Faker

from employees.models import Employee

COUNTRIES = {
    "India": ("INR", 400_000, 3_000_000),
    "USA": ("USD", 50_000, 220_000),
    "UK": ("GBP", 35_000, 150_000),
    "Germany": ("EUR", 40_000, 160_000),
    "Singapore": ("SGD", 45_000, 180_000),
}
JOB_TITLES = [
    "Software Engineer", "Senior Engineer", "QA Engineer", "Product Manager",
    "Designer", "Data Analyst", "HR Executive", "Sales Executive",
    "Accountant", "Engineering Manager",
]
DEPARTMENTS = ["Engineering", "Product", "Design", "HR", "Sales", "Finance"]


class Command(BaseCommand):
    help = "Seed the database with 10,000 employees"

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=10_000)

    def handle(self, *args, **options):
        fake = Faker()
        Faker.seed(42)
        random.seed(42)

        Employee.objects.all().delete()
        employees = []
        for i in range(options["count"]):
            country = random.choice(list(COUNTRIES))
            currency, low, high = COUNTRIES[country]
            employees.append(Employee(
                full_name=fake.name(),
                email=f"user{i}@acme.com",
                job_title=random.choice(JOB_TITLES),
                department=random.choice(DEPARTMENTS),
                country=country,
                currency=currency,
                salary=Decimal(random.randint(low, high)),
                date_joined=date.today() - timedelta(days=random.randint(30, 3650)),
            ))
        Employee.objects.bulk_create(employees, batch_size=1000)
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(employees)} employees"))