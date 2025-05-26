from django.urls import path
from .views import (
    CommentReportListCreateView,
    CommentReportDetailView,
    CommentReportsByCommentIdView
)

urlpatterns = [
    path('', CommentReportListCreateView.as_view(), name='comment-report-list-create'),
    path('<int:pk>/', CommentReportDetailView.as_view(), name='comment-report-detail'),
    path('by-comment/<int:comment_id>/', CommentReportsByCommentIdView.as_view(), name='comment-reports-by-comment-id'),
]
