from rest_framework.routers import DefaultRouter
from .views import ProjectReportViewSet

router = DefaultRouter()
router.register(r'project-reports', ProjectReportViewSet)

urlpatterns = router.urls
