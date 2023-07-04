
from django.db.models import Count, Q
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, CreateAPIView, DestroyAPIView

from ads.models import User
from ads.serialazers import UserSerializer, UserListSerializer, UserCreateUpdateSerializer


class UserListView(ListAPIView):
    queryset = User.objects.annotate(total_ads=Count("ad", filter=Q(ad__is_published=True))).order_by(
        'username')
    serializer_class = UserListSerializer


class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateUpdateSerializer


class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateUpdateSerializer


class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
