from rest_framework import filters
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from .models import Category, Tag, Post
from .permissions import IsAdminPermission, IsAuthorPermission
from .serializers import CategorySerializer, TagSerializer, PostSerializer

class CategoriesListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # pagination_class =

class TagsListView(ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class PostsListView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

# фильтрация
# api/v1/posts/tag/
# api/v1/posts?tags=sport, ...
class PostViewSet(ModelViewSet):
    queryset = Post.objects.all() # order_by('created_at') -created_ad DESC
    serializer_class = PostSerializer
    lookup_url_kwarg = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'text', 'tags__title']

    def get_permissions(self):
        if self.action == 'create':
            permissions = [IsAdminPermission]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsAuthorPermission]
        else:
            permissions = []
        return [perm() for perm in permissions]

    def get_queryset(self):
        queryset = super().get_queryset()
        tags = self.request.query_params.get('tags')
        if tags is not None:
            tags = tags.split(',')
            queryset = queryset.filter(tags__slug__in=tags)
        return queryset


# POST - create
# GET - list, retrieve(details)

# api/v1/post - create, list
# api/v1/post/<id/slug> - details, update, delete

# PUT, PATCH - update
# DELETE - destroy

# TODO: переделать фильтрацию
# TODO: сделать документацию
# TODO: сделать восстановление и смену пароля
# TODO: избраннное (лайки)
# TODO: комментарии
