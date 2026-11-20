from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import EmployeeViewSet, insights_by_country, insights_by_job_title

router = DefaultRouter()
router.register("employees", EmployeeViewSet)

urlpatterns = [
    path("insights/by-country/", insights_by_country),
    path("insights/by-job-title/", insights_by_job_title),
] + router.urls