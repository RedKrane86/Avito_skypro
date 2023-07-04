from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet

from ads.models import Selection
from ads.permissions import IsOwner
from ads.serialazers import SelectionSerializer, SelectionCreateSerializer


class SelectionViewSet(ModelViewSet):
    queryset = Selection.objects.all()
    serializers = {
        'Create': SelectionCreateSerializer,
    }
    default_serializer = SelectionSerializer

    permissions = {
        'retrieve': [IsAuthenticated],
        'create': [IsAuthenticated],
        'update': [IsOwner],
        'partial_update': [IsOwner],
        'destroy': [IsOwner]
    }
    default_permission = [AllowAny]

    def get_permissions(self):
        self.permission_classes = self.permissions.get(self.action, self.default_permission)
        return super().get_permissions()

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer)