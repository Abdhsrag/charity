from rest_framework import serializers
from comments.models import Comments

class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    # NOT TO TEST THE REPLAY YOU HAVE TO INCLUDE THE PARENT AND CONTENT FIELDS THE PARENT == THE COMMENT ID
    class Meta:
        model = Comments
        fields = ['content', 'date', 'parent', 'replies']

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []