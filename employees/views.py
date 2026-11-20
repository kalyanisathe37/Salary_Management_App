from rest_framework import viewsets, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Employee
from .serializers import EmployeeSerializer
from .insights import salary_stats


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all().order_by("id")
    serializer_class = EmployeeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["full_name", "email"]

    def get_queryset(self):
        qs = super().get_queryset()
        country = self.request.query_params.get("country")
        job_title = self.request.query_params.get("job_title")
        if country:
            qs = qs.filter(country=country)
        if job_title:
            qs = qs.filter(job_title=job_title)
        return qs


@api_view(["GET"])
def insights_by_country(request):
    return Response(salary_stats("country"))


@api_view(["GET"])
def insights_by_job_title(request):
    return Response(salary_stats("job_title"))