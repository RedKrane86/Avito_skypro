
from rest_framework.viewsets import ModelViewSet


from ads.models import Category
from ads.serialazers import CategorySerializer


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
