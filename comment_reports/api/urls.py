from rest_framework.routers import DefaultRouter
from .views import CommentReportViewSet

router = DefaultRouter()
router.register(r'comment-reports', CommentReportViewSet)

urlpatterns = router.urls
