from collections import defaultdict
from statistics import median

from django.db.models import Avg, Count, Max, Min

from .models import Employee


def salary_stats(group_field):
    """Salary stats grouped by `group_field` (country or job_title) and currency."""
    rows = (
        Employee.objects.values(group_field, "currency")
        .annotate(count=Count("id"), min=Min("salary"), max=Max("salary"), avg=Avg("salary"))
        .order_by(group_field, "currency")
    )

    salaries = defaultdict(list)
    for key, currency, salary in (
        Employee.objects.order_by("salary").values_list(group_field, "currency", "salary")
    ):
        salaries[(key, currency)].append(salary)

    return [
        {
            group_field: r[group_field],
            "currency": r["currency"],
            "count": r["count"],
            "min": float(r["min"]),
            "max": float(r["max"]),
            "avg": round(float(r["avg"]), 2),
            "median": float(median(salaries[(r[group_field], r["currency"])])),
        }
        for r in rows
    ]