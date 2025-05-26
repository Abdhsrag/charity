from rest_framework import serializers
from comments.models import Comments

class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comments
        fields = ['content', 'date', 'parent', 'replies']

    def get_replies(self, obj):
        return [
            {
                "content": reply.content,
                "date": reply.date,
                "parent": reply.parent_id,
            }
            for reply in obj.replies.all()
        ]