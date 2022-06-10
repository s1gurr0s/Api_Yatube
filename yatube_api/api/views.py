from django.shortcuts import get_object_or_404
from posts.models import Comment, Group, Post
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from .serializers import CommentSerializer, GroupSerializer, PostSerializer

NO_CHANGES = 'Изменение чужого контента запрещено!'
NO_DELETE = 'Удаление чужого контента запрещено!'


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied(NO_CHANGES)
        super(PostViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied(NO_DELETE)
        super(PostViewSet, self).perform_destroy(instance)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs['post_pk'])
        return Comment.objects.filter(post=post)

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs['post_pk'])
        serializer.save(author=self.request.user, post=post)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied(NO_CHANGES)
        super(CommentViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied(NO_DELETE)
        super(CommentViewSet, self).perform_destroy(instance)
