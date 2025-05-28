from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from comments.models import Comments
from .serializers import CommentSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": "All good", "data": serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {"detail": "Not found."},
                status=status.HTTP_404_NOT_FOUND
            )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            {"message": "Comment updated", "data": serializer.data},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'])
    def top_level(self, request):
        comments = Comments.objects.filter(parent__isnull=True)
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def replies(self, request):
        replies = Comments.objects.filter(parent__isnull=False)
        serializer = self.get_serializer(replies, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='by-project/(?P<project_id>[^/.]+)')
    def by_project(self, request, project_id=None):
        comments = Comments.objects.filter(project_id=project_id, parent__isnull=True)
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='by-user/(?P<user_id>[^/.]+)')
    def by_user(self, request, user_id=None):
        comments = Comments.objects.filter(user_id=user_id, parent__isnull=True)
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data)