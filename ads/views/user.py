import json

from django.db.models import Count, Q
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, CreateView, ListView, DeleteView, UpdateView
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, CreateAPIView, DestroyAPIView

from HW_27 import settings
from ads.models import User, Location
from ads.serialazers import UserSerializer, UserListSerializer, UserCreateUpdateSerializer


# class UserListView(ListView):
#     model = User
#
#     def get(self, request, *args, **kwargs):
#         super().get(request, *args, **kwargs)
#
#         users = User.objects.annotate(total_ads=Count("ad", filter=Q(ad__is_published=True)))
#
#         total_users = self.object_list.count()
#         page = int(request.GET.get("page", 0))
#         offset = page * settings.TOTAL_ON_PAGE
#
#         if offset > total_users:
#             self.object_list = []
#         elif offset:
#             self.object_list = self.object_list[offset:settings.TOTAL_ON_PAGE]
#         else:
#             self.object_list = self.object_list[:settings.TOTAL_ON_PAGE]
#
#         result = []
#         for user in users:
#             result.append({
#                 "id": user.id,
#                 "username": user.username,
#                 "first_name": user.first_name,
#                 "last_name": user.last_name,
#                 "role": user.role,
#                 "age": user.age,
#                 "locations": user.location.name,
#                 "total_ads": user.total_ads
#             })
#
#         response = {
#             "items": result,
#             "total": total_users,
#             "per_page": settings.TOTAL_ON_PAGE
#         }
#
#         return JsonResponse(response, safe=False)


# class UserDetailView(DetailView):
#     model = User
#
#     def get(self, request, *args, **kwargs):
#         user = self.get_object()
#
#         return JsonResponse({
#                 "id": user.id,
#                 "username": user.username,
#                 "first_name": user.first_name,
#                 "last_name": user.last_name,
#                 "role": user.role,
#                 "age": user.age,
#                 "locations": user.location.name
#             })


# @method_decorator(csrf_exempt, name='dispatch')
# class UserCreateView(CreateView):
#     model = User
#     fields = "__all__"
#
#     def post(self, request, *args, **kwargs):
#         user_data = json.loads(request.body)
#
#         location = Location.objects.get_or_create(name=user_data.pop("location"))
#         new_user = User.objects.create(location=location, **user_data)
#         locations = user_data.pop("location")
#
#         for loc_name in locations:
#             loc, _ = Location.objects.get_or_create(name=loc_name)
#             new_user.location.add(loc)
#
#         return JsonResponse({
#             "id": new_user.id,
#             "username": new_user.username,
#             "first_name": new_user.first_name,
#             "last_name": new_user.last_name,
#             "role": new_user.role,
#             "age": new_user.age,
#             "locations": new_user.location.name
#         })


# @method_decorator(csrf_exempt, name='dispatch')
# class UserUpdateView(UpdateView):
#     model = User
#     fields = "__all__"
#
#     def patch(self, request, *args, **kwargs):
#         super().post(self, request, *args, **kwargs)
#         data = json.loads(request.body)
#         if "username" in data:
#             self.object.username = data.pop("username")
#         if "password" in data:
#             self.object.password = data.pop("password")
#         if "first_name" in data:
#             self.object.first_name = data.pop("first_name")
#         if "last_name" in data:
#             self.object.last_name = data.pop("last_name")
#         if "age" in data:
#             self.object.age = data.pop("age")
#         if "locations" in data:
#             self.object.locations = data.pop("locations")
#
#         self.object.save()
#
#         user = self.get_object()
#
#         return JsonResponse({
#             "id": user.id,
#             "username": user.username,
#             "first_name": user.first_name,
#             "last_name": user.last_name,
#             "role": user.role,
#             "age": user.age,
#             "locations": user.location.name
#         })


# @method_decorator(csrf_exempt, name='dispatch')
# class UserDeleteView(DeleteView):
#     model = User
#     success_url = "/"
#
#     def delete(self, request, *args, **kwargs):
#         super().delete(request, *args, **kwargs)
#
#         return JsonResponse({
#             "status": "ok"
#         })


class UserListView(ListAPIView):
    queryset = User.objects.annotate(total_ads=Count("ad", filter=Q(ad__is_published=True)))
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
