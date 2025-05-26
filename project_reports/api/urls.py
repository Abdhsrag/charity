from django.urls import path
from .views import (
    ProjectReportListCreateView,
    ProjectReportDetailView,
    ProjectReportsByProjectIdView,
)

urlpatterns = [
    path('', ProjectReportListCreateView.as_view(), name='project-report-list-create'),
    path('<int:pk>/', ProjectReportDetailView.as_view(), name='project-report-detail'),
    path('by-project/<int:project_id>/', ProjectReportsByProjectIdView.as_view(), name='project-reports-by-project-id'),
]
