from posts.models import Comment, Group, Post
from rest_framework import serializers


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'title', 'slug')


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    group = serializers.SlugRelatedField(
        queryset=Group.objects.all(),
        required=False,
        slug_field='slug'
    )

    class Meta:
        model = Post
        fields = ('id', 'text', 'pub_date', 'author', 'group')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')
